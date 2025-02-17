import json
import os
import os.path as osp

import numpy as np
from tqdm import tqdm
import sys
from urllib.request import urlopen
sys.path.append('Pointing to the project root directory')
from metric import judge_wer_speechGPT as judge_wer
from metric import judge_multiple_choice
from metric import judge_yes_no
from metric import judge_wer_find as judge_song_asr
from metric import has_judge

# Perhaps you can add some initialization specific to the model here.
# Import the packages required for Qwen2-Audio.
from io import BytesIO
import librosa
from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor

# Perform the initialization required for Qwen2-Audio.
processor = AutoProcessor.from_pretrained("~/model_cache/Qwen2-Audio-7B-Instruct")
model = Qwen2AudioForConditionalGeneration.from_pretrained("~/model_cache/Qwen2-Audio-7B-Instruct", device_map="auto")

def input_single_audio(audio_path, question):
    """
    Implement the inference process for Qwen2-Audio.
    :param audio_path:
    :param question:
    :return:
    """
    conversation = [
        {"role": "assistant",
         "content": "Stay alert and cautious, and check if anyone is hurt or if there is any damage to property."},
        {"role": "user", "content": [
            {"type": "audio",
             "audio_url": "file:%s" % audio_path},
            {"type": "text", "text": question},
        ]},
    ]
    text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios = []
    try:
        audios.append(
            librosa.load(
                BytesIO(urlopen("file:%s" % audio_path).read()),
                sr=processor.feature_extractor.sampling_rate)[0]
        )
    except Exception as e:
        # Try to respect the original author's use of URL to load data, but if errors occur, direct loading must be used instead.
        y, sr = librosa.load(audio_path)
        audios.append(y)
    inputs = processor(text=text, audios=audios, return_tensors="pt", padding=True)
    inputs.input_ids = inputs.input_ids.to("cuda")
    inputs.to("cuda")
    # model.to("cuda")

    generate_ids = model.generate(**inputs, max_length=256)
    generate_ids = generate_ids[:, inputs.input_ids.size(1):]

    response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return response, response

result_path = "Point to the path where you want the result to be saved."
os.makedirs(result_path,exist_ok=True)

def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    with open(osp.join(result_path, json_filename), 'w') as f:
        json.dump(dump_data, f)


def deal_single_audio_question(question_json_path, experiment_sign, question_type, question):
    assert question_type in ['true_false', "has",'wer', 'no_judge', 'no_judge_emoT',"song_wer", 'multiple_choice']
    question_label = osp.basename(question_json_path.split('.')[0])

    with open(question_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    detail_list = list()
    result_list = list()

    for i, sample in tqdm(enumerate(data)):
        # print(sample['voice_absolute_path'])
        output, detail = input_single_audio(
            audio_path=sample['voice_absolute_path'],
            question=question if question is not None else sample['question'],
        )
        
        if question_type == 'true_false':
            judge_result = judge_yes_no(sample['answer'], output)
        elif question_type == "wer":
            judge_result = judge_wer(sample['answer'], output)
        elif question_type == "song_wer":
            judge_result = judge_song_asr(sample['answer'], output)
        elif question_type == "has":
            judge_result = has_judge(sample['answer'], output)
        elif question_type == "multiple_choice":
            judge_result = judge_multiple_choice(sample['answer'], output)
        elif question_type == 'no_judge':
            judge_result = 'no_judge'
        elif question_type == 'no_judge_emoT':
            judge_result = sample["discript"]
        else:
            raise ValueError("question_type error")

        detail_list.append(dict(
            lalm_answer=output,
            question=question if question is not None else sample['question'],
            label_answer=sample['answer'],
            voice_absolute_path=sample['voice_absolute_path'],
            detail=detail,
            judge=judge_result,
        ))
        if i % 1 == 0:
            # 20个一保存
            dump_json(question_label + experiment_sign + ".json", detail_list)

        if question_type in ["has",'true_false', 'multiple_choice']:
            if judge_result:
                result_list.append(1)
            else:
                result_list.append(0)
        elif question_type in ["song_wer", "wer"]:
            result_list.append(judge_result)
        elif question_type in ['no_judge','no_judge_emoT']:
            result_list.append(judge_result)
        else:
            raise ValueError("question_type error")

    if question_type in ["has",'true_false', 'multiple_choice']:
        result = round(sum(np.array(result_list)) / len(result_list), 4) * 100
    elif question_type in ["song_wer", "wer"]:
        result = round(np.mean(np.array(result_list)), 4)
    elif question_type in ['no_judge', 'no_judge_emoT']:
        result = "no_judge"
    else:
        raise ValueError("question_type error")
    dump_json(question_label + "_" +  experiment_sign + "_" + str(result) + ".json", detail_list)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--question_json_path', default="",
                        help='Absolute path to json path')

    parser.add_argument('--experiment_sign', default="",
                        help='The sign for this experiment')

    parser.add_argument('--question_type', default="",
                        help='Specify the evaluation method that the model needs to use.')

    parser.add_argument('--question', default=None,
                        help='Through this, you can forcibly modify the input question, which will overwrite the question in the JSON file.')

    args = parser.parse_args()

    deal_single_audio_question(
        question_json_path=args.question_json_path,
        experiment_sign=args.experiment_sign,
        question_type=args.question_type,
        question=args.question,
    )
