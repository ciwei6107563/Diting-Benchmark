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

result_path = "Point to the path where you want the result to be saved."
os.makedirs(result_path,exist_ok=True)

def input_single_audio(audio_path, question):
    """
    您需要再整理实现
    :param audio_path:
    :param question:
    :return:
    """
    output = "The model's output"
    detail = "Other details you want to save for analysis"
    return output, detail


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
