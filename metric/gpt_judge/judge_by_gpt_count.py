# coding: utf-8
import numpy as np
import openai
import traceback
import time
import json
import re

DEBUG = False

# openai.log = "debug"
openai.api_key = ""  # Enter the address provided by your service provider: Enter the API key we provided to you.
openai.api_base = "" # Enter the address of your service provider.

openai.proxy = {
    "http": None,
    "https": None
}


class GetOpenAI:
    @staticmethod
    def __gpt_api_stream(messages: list, model='gpt-4'):
        """
        Args:
            messages (list): 完整的对话消息
            api_key (str): OpenAI API 密钥

        Returns:
            tuple: (results, error_desc)
        """
        completion = {'role': '', 'content': ''}
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=True,
                # max_tokens=7000,
                # temperature=0.5,
                # presence_penalty=0,
            )
            for event in response:
                if event['choices'][0]['finish_reason'] == 'stop':
                    if DEBUG:
                        pass
                        # print(f'收到的完成数据: {completion}')
                    break
                for delta_k, delta_v in event['choices'][0]['delta'].items():
                    if DEBUG:
                        print(f'流响应数据: {delta_k} = {delta_v}')
                    completion[delta_k] += delta_v
            messages.append(completion)  # 直接在传入参数 messages 中追加消息
            msg = completion['content']  # 解析返回的msg
            return (True, msg)
        except Exception as err:
            if DEBUG:
                print(f"{traceback.format_exc()}")
            return (False, f'OpenAI API 异常: {err} {completion}')

    def get_respons(self, input_msg, model="gpt-3.5-turbo"):
        assert model in ["gpt-3.5-turbo", 'gpt-4', "gpt-4-turbo-2024-04-09", "gpt-4o-2024-05-13", 'gpt-4o']
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {'role': 'user', 'content': input_msg}]
        for _ in range(3):
            ret, out_msg = self.__gpt_api_stream(messages, model=model)  # 流模式调用
            if ret:
                break
            else:
                # api 不能频繁请求
                time.sleep(1)

        return ret, out_msg


def judge_voice_detective(result_path):
    openai_tool = GetOpenAI()
    base_input_msg = """
    I now need you to help me evaluate some Answers for accuracy.
    You should focus on whether the information about gender, place of birth, age, and native language in the Answer matches the Label, and provide a final rating.
    Award 1 point for each correct piece of information, with no points for incorrect information. Please give your score on a scale of 0 to 4.
    Here are some examples:
    1.
    Answer:The speaker is male and his age is not mentioned in the caption.
    Label:The person is a female born in virginia, south africa in the 'teens to twenties' age group.And native_language is afrikaans.
    You should answer:score:0
    2.
    Answer:The speaker's gender is male or female. The place of birth is not specified. The age cannot be determined from the audio clip. The native language is not specified.
    Label:The person is a female born in virginia, south africa in the 'teens to twenties' age group.And native_language is afrikaans.
    You should answer:score:0
    3.
    Answer:The speaker's gender is male. The place of birth is not specified. The age cannot be determined from the audio clip. The native language is not specified.
    Label:The person is a female born in virginia, south africa in the 'teens to twenties' age group.And native_language is afrikaans.
    You should answer:score:1
    4.
    Answer:The speaker is a man speaking, in a English, saying, 'Please call Stela and ask her to bring these things with her from the store. Six spoons of free snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob. We also need a small plastic snake and a big toy frog for the kids. She can scoop these things into three red bags and we will go meet her Wednesday at the train station.'."
    Label:The person is a male born in virginia, south africa in the 'teens to twenties' age group.And native_language is afrikaans.
    You should answer:score:1
    5.
    Answer:"The speaker is a 28-year-old female speaking English with an Australian accent."
    Label:The person is a male born in mitrovice, kosovo in the 'thirties to forties' age group.And native_language is albanian.
    You should answer:score:0
    6.
    Answer:"The speaker is a 34-year-old male speaking English with an Australian accent."
    Label:The person is a male born in mitrovice, kosovo in the 'thirties to forties' age group.And native_language is albanian.
    You should answer:score:2
    7.
    Answer:"The speaker is a 34-year-old male speaking English with an albanian accent."
    Label:The person is a male born in mitrovice, kosovo in the 'thirties to forties' age group.And native_language is albanian.
    You should answer:score:3
    8.
    Answer:"A 34-year-old male from Mitrovice, Kosovo, speaks English with an Albanian accent."
    Label:The person is a male born in mitrovice, kosovo in the 'thirties to forties' age group.And native_language is albanian.
    You should answer:score:4
    Now Answer:[ANSWER]
    Label:[LABEL]
    Please provide your score.
    """
    with open(result_path, 'r') as f:
        result_datas = json.load(f)
    result_list = list()
    # 正则表达式匹配模式
    pattern = r"(?i)score:\s*(\d+)"

    for result_data in result_datas:
        matches = re.findall(pattern, result_data["judge"])
        while len(matches) == 0:
            print(len(result_list))
            input_msg = base_input_msg.replace(
                '[ANSWER]', result_data["lalm_answer"]
            ).replace("[LABEL]", result_data["label_answer"])
            ref, out_msg = openai_tool.get_respons(input_msg, model='gpt-4o')
            result_data["judge"] = out_msg
            matches = re.findall(pattern, result_data["judge"])
            print(out_msg)
        result_list.append(float(matches[0]))
        with open(result_path.replace("gpt_judge", "gpt_judge_count"), 'w') as f:
            json.dump(result_datas, f)

    result = np.mean(np.array(result_list))

    with open(result_path.replace(".json", "gpt_judge_%s.json" % result), 'w') as f:
        json.dump(result_datas, f)


def judge_spoken_english_coach(result_path):
    openai_tool = GetOpenAI()
    base_input_msg = """
    I now need you to help me evaluate some Answers for accuracy.
    You need to evaluate and score in the order of overall pronunciation, fluency, prosody, words that are mispronounced, and words that have incorrect stress. The score ranges from 0 to 4. Here are the specific scoring rules:
    You need to first check if the evaluation of overall pronunciation in the Answer matches the Label. If they do not match, give a score of 0 and continue with the evaluation; if there is no relevant description, also give a score of 0 and continue with the evaluation; if it is correct, add 1 point and continue with the evaluation.
    For fluency and prosody in the Answer compared to the Label, award up to 1 point for each if completely correct, a partial score for partially correct, and no points if there is no relevant expression.
    Finally, check the descriptions in the Answer and Label regarding words that are mispronounced and words that have incorrect stress. Award 1 point only if all are correct. If part of the descriptions are correct, you can give a partial score, such as 0.33 points for one out of three correct descriptions.
    Here are some examples:
    1.
    Answer:"The overall pronunciation is good, with clear enunciation of each word. Fluency is moderate, with occasional pauses between words. Prosody is normal, with appropriate intonation and rhythm. There are no mispronounced words or words with incorrect stress."
    Label:"The overall pronunciation of the sentence is poor, clumsy and rigid pronunciation of the sentence as a whole, with serious pronunciation mistakesFor fluency:the speech is a little influent, with many pauses, repetition, and stammeringFor prosodic:Unstable speech speed, many stammering and pauses with a poor sense of rhythmFor words:More than 30% of phones in word HER are wrongly pronouncedMore than 30% of phones in word HER are wrongly pronouncedMore than 30% of phones in word WATCH are wrongly pronounced"
    Because:The evaluations for overall pronunciation, fluency, prosody and word mistake are not consistent, so no points are awarded.
    You should answer:score:0
    2.
    Answer:The overall pronunciation is correct but some parts seem to be delivered in a more casual manner, indicative of English spoken by a non-native with a regional accent. Fluency is good, but there are occasional hesitations and pauses. Prosody is also acceptable; however, the intonation sometimes lags behind the word's enunciation. There are no major errors in stress, but some syllables are pronounced with slightly different accents than standard English.\n\nWords with incorrect stress:\nnone\n\nMispronounced words:\n'around' should be 'aound'\n\nWord order and phrasing may vary in casual speech, so these adjustments do not significantly alter the meaning of the sentence.
    Label:The overall pronunciation of the sentence is understandable, with many pronunciation mistakes and accent, but it does not affect the understanding of basic meaningsFor fluency:Fluent in general, with a few pauses, repetition, and stammeringFor prosodic:Unstable speech speed, many stammering and pauses with a poor sense of rhythmFor words:More than 30% of phones in word IT'S are wrongly pronouncedMore than 30% of phones in word AROUND are wrongly pronouncedLess than 30% of phones in word PLACE are wrongly pronounced
    Because:For this pair of Answer and Label: receive 1 point for the overall pronunciation being essentially the same. Receive 1 point each for fluency and prosody evaluations being largely consistent, totaling 2 points.Successfully identified one of the two incorrect words, "round," but the identified error was incorrect, earning 0.2 points.
    You should answer:score:3.2
    3.
    Answer:The overall pronunciation is good, with clear articulation of each word. Fluency is also good, with a smooth flow between words. 
    Label:The overall pronunciation of the sentence is excellent, with accurate phonology and no obvious pronunciation mistakesFor fluency:Fluent without noticeable pauses or stammeringFor prosodic:Correct intonation at a stable speaking speed, speak with cadence, and can speak like a native
    Because:The evaluations for overall pronunciation and fluency are correct, earning 1 point each. The remaining information was not mentioned, so no points are awarded for that.
    You should answer:score:2
    4.
    Answer:The overall pronunciation is correct with some minor variations in intonation. Fluency is good as the speech is delivered smoothly without any pauses or hesitations. Prosody is also good as the rhythm and stress patterns align well with the language's natural flow.There are no mispronounced words in this segment. However, the word 'ending' has an incorrect stress pattern; it should be stressed on the second syllable ('en-ding') rather than the first ('en-din').
    Label:The overall pronunciation of the sentence is understandable, with many pronunciation mistakes and accent, but it does not affect the understanding of basic meaningsFor fluency:the speech is a little influent, with many pauses, repetition, and stammeringFor prosodic:Unstable speech speed, many stammering and pauses with a poor sense of rhythmFor words:More than 30% of phones in word PERFECT are wrongly pronouncedLess than 30% of phones in word ENDING are wrongly pronounced
    Because:The evaluations for overall pronunciation, fluency, and prosody are not consistent, so no points are awarded. However, one of the two word errors was successfully identified, although the specific error was incorrect, earning 0.2 points.
    You should answer:score:0.2
    5.
    Answer:The overall pronunciation is quite poor with noticeable errors in enunciation and intonation. There seems to be a struggle with the production of certain sounds, particularly the 'th' sound, which is often replaced by other consonants. Additionally, the speech lacks fluency as the words are spoken at a slow pace and there's a noticeable hesitation between syllables. The prosody is also affected; the rhythm appears to be off kilter, and there's a lack of variation in pitch and volume. Words such as 'people' and 'ship' are consistently pronounced incorrectly, with 'people' being frequently pronounced with a hard 'p' sound instead of the correct soft 'p' sound heard in standard English. Furthermore, the stress on words like
    Label:The overall pronunciation of the sentence is excellent, with accurate phonology and no obvious pronunciation mistakesFor fluency:Fluent without noticeable pauses or stammeringFor prosodic:Correct intonation at a stable speaking speed, speak with cadence, and can speak like a nativeFor words:
    Because:The evaluations for overall pronunciation, fluency, prosody and word mistake are not consistent, so no points are awarded.
    You should answer:score:0
    6.
    Answer:The overall pronunciation is correct but the stress on certain words is not as expected. 'There' is pronounced with the correct stress on the first syllable ('thEr'), but 'so' has an incorrect stress pattern ('sOh'). Additionally, 'that' is pronounced with the stress on the second syllable ('thAt'), which should be 'thaT'. Fluency is good, and the prosody is regular and easy to follow."
    Label:The overall pronunciation of the sentence is poor, clumsy and rigid pronunciation of the sentence as a whole, with serious pronunciation mistakesFor fluency:the speech is a little influent, with many pauses, repetition, and stammeringFor prosodic:Unstable speech speed, speak too fast or too slow, without the sense of rhythmFor words:More than 30% of phones in word WAS are wrongly pronouncedMore than 30% of phones in word SO are wrongly pronouncedMore than 30% of phones in word MUCH are wrongly pronouncedMore than 30% of phones in word IT are wrongly pronouncedMore than 30% of phones in word THAT are wrongly pronounced
    Because:The evaluations for overall pronunciation, fluency, prosody are not consistent, so no points are awarded.However, two out of five word-level errors were successfully identified, but the error descriptions were incorrect, therefore each earns 0.1 points.
    You should answer:score:0.2
    7.
    Answer:The overall pronunciation is quite poor, with noticeable errors in intonation, stress, and word sounds. Fluency is also lacking as the speech is broken and hesitant. Prosody is non-existent as there's no rhythmic pattern in the speech. Words like 'play' and 'with' are correctly pronounced but words like 'are', 'you', and 'me' have incorrect stress and some syllable errors.
    Label:The overall pronunciation of the sentence is poor, clumsy and rigid pronunciation of the sentence as a whole, with serious pronunciation mistakesFor fluency:the speech is a little influent, with many pauses, repetition, and stammeringFor prosodic:Unstable speech speed, speak too fast or too slow, without the sense of rhythmFor words:More than 30% of phones in word SO are wrongly pronouncedMore than 30% of phones in word HERE are wrongly pronouncedMore than 30% of phones in word WITH are wrongly pronouncedMore than 30% of phones in word ME are wrongly pronounced
    Because:The evaluations for overall pronunciation, fluency, and prosody are consistent, earning 1 point each, for a total of 3 points. However, none of the word errors were correctly identified, so no points are awarded for that.
    You should answer:score:3
    8.
    Answer:The overall pronunciation of the sentence is poor, clumsy and rigid pronunciation of the sentence as a whole, with serious pronunciation mistakesFor fluency:the speech is a little influent, with many pauses, repetition, and stammeringFor prosodic:Unstable speech speed, speak too fast or too slow, without the sense of rhythmFor words: The stress of the word ACCEPTED is incorrect.The stress of the word TETHINGS is incorrect.
    Label:The overall pronunciation is quite poor with noticeable errors in enunciation and intonation.Fluency is also an issue as the speech seems not well-paced. Additionally, there are problems with prosody as the rhythm and stress patterns do not follow standard English conventions.there are two words with incorrect stress: 'accepted' should be stressed on the second syllable ('acCEPTED'), and 'things' should be stressed on the first syllable ('THiNGs').
    Because:All information (overall pronunciation, fluency, prosody, and word mistakes) was mentioned and judged consistently, so full points are awarded.
    You should answer:score:4
    Now Answer:[ANSWER]
    Label:[LABEL]
    Please provide your score.
    """
    with open(result_path, 'r') as f:
        result_datas = json.load(f)
    result_list = list()
    # 正则表达式匹配模式
    pattern = r"(?i)score:\s*([\d.]+)"

    for result_data in result_datas:
        matches = re.findall(pattern, result_data["judge"].replace("*", ""))
        while len(matches) == 0:
            print(len(result_list))
            input_msg = base_input_msg.replace(
                '[ANSWER]', result_data["lalm_answer"]
            ).replace("[LABEL]", result_data["label_answer"])
            ref, out_msg = openai_tool.get_respons(input_msg, model='gpt-4o')
            result_data["judge"] = out_msg
            # 去除加粗
            out_msg = out_msg.replace("*", "")
            matches = re.findall(pattern, out_msg)
            print(out_msg)
        score = matches[-1]  # 最后的是经过深思熟路的结果
        if score[-1] == ".":
            score = score[:-1]
        score = float(score)
        result_data["score"] = score
        result_list.append(score)
        with open(
                result_path.replace(
                    "gpt_judge", "gpt_judge_count"),
                'w') as f:
            json.dump(result_datas, f)

    result = np.mean(np.array(result_list))

    with open(
            result_path.replace(
                "gpt_judge", "gpt_judge_%s" % result).replace(
                "gpt_judge_count", "gpt_judge_%s" % result),
            'w') as f:
        json.dump(result_datas, f)


def judge_emotion_translate(result_path):
    openai_tool = GetOpenAI()
    base_input_msg = """
    I currently need your assistance in evaluating some translations. The most suitable translations should incorporate the corresponding emotions appropriately. The scoring ranges from 0 to 4. I will provide you with the original English sentence, the associated emotional label, and the suggested translation, allowing you to score them based on the context.
    For example: The original sentence is: "<sad>You have to trust me." The suggested translation is: "求你一定相信我". This expresses "You have to trust me" in a sad tone, and it is recommended to translate it considering this emotion as: "求你一定相信我".
    
    Here are some scoring examples:
    1.
    Answer:"这个句子的中文翻译可能是：'我不想谈论它。'"
    Label:The original sentence is: "<sad>I don't want to talk about it." The suggested translation is: "我不想谈这个，我真的很难过。".
    Because:The translation is completed, but it fails to convey the appropriate emotion, earning 1 point.
    You should answer:score:1
    2.
    Answer: "这个句子的中文翻译可能是：'他们不想谈论它。'",
    Label:The original sentence is: "<angry>I don't want to talk about it." The suggested translation is: "我不想谈这个，别再问了！"
    Because:The translation was done but incorrect, earning no points.
    You should answer:score:0
    3.
    Answer:"这个音频片段的情感和内容需要根据具体情况来确定最合适的中文翻译。"
    Label:The original sentence is: "<angry>Please don't leave." The suggested translation is:   "不要走，听到没有！"
    Because:No translation was performed, earning no points.
    You should answer:score:0
    4.
    Answer:"这个音频片段的情感和内容表明，最合适的中文翻译可能是“现在太晚了”"
    Label:The original sentence is: "<angry>It's too late now." The suggested translation is: "这个音频片段的情感和内容表明，最合适的中文翻译可能是“现在太晚了。”"
    Because:The translation is completed, but it fails to convey the appropriate emotion, earning 1 point.
    You should answer:score:1
    5.
    Answer:"这个音频片段的情感是愤怒的，内容是'你为什么不告诉我！'。根据这些信息，最合适的中文翻译可能是'你为什么没有告诉我！'。",
    Label:The original sentence is: "<angry>Why didn’t you tell me?" The suggested translation is: "你为什么不告诉我？！太过分了！",.
    Because:Although it differs from the suggested translation, the emotion is accurately conveyed, deserving 4 points.
    You should answer:score:4
    6.
    Answer:"The translation in Chinese is: '让我一个人呆着！'"
    Label:The original sentence is: "<angry>Leave me alone." The suggested translation is: "别烦我了，走开！".
    Because:Emotion is conveyed only through punctuation, while the rest of the content remains consistent with a direct translation, earning 2 points.
    You should answer:score:2
    7.
    Answer:"这个音频片段表达的是悲伤或同情的情绪，所以最合适的中文翻译可能是“一切都结束了。”或者“一切已经过去了。”",
    Label:The original sentence is: "<angry>It’s over." The suggested translation is: "结束了！我们之间完了！".
    Because:识别出了情感，但是对应的情感不对，只得1分。
    You should answer:score:1
    8.
    Answer: "这个音频片段表达的是惊讶的情感，所以最合适的中文翻译是“我简直无法相信。”",
    Label:The original sentence is: "<surprised>I can't believe it." The suggested translation is: "我真不敢相信这是真的！",.
    Because:Although it differs from the suggested translation, the emotion is accurately conveyed, deserving 4 points.
    You should answer:score:4
    9.
    Answer: "这个音频片段表达的是愤怒和沮丧，所以最合适的中文翻译可能是：'我再也不能做这件事了！'"
    Label:The original sentence is: "<angry>I can't do this anymore." The suggested translation is:  "我受够了，再也不想这样做了！",.
    Because:The emotion was correctly identified, but the translation was not adjusted based on the emotion, earning 2 points.
    You should answer:score:2
    10.
    Answer: "这个音频片段的情感是悲伤的，内容是'一切都结束了。'所以最合适的中文翻译可能是'一切都结束了。'"
    Label:The original sentence is: "<angry>It’s over." The suggested translation is:  "结束了！我们之间完了！",.
    Because:The corresponding emotion was recognized, but incorrectly, earning only 1 point.
    You should answer:score:1
    Now Answer:[ANSWER]
    Label:The original sentence is: [SENTENCE]  
    Please provide your score.
    """
    with open(result_path, 'r') as f:
        result_datas = json.load(f)
    result_list = list()
    # 正则表达式匹配模式
    pattern = r"(?i)score:\s*([\d.]+)"

    for result_data in result_datas:
        matches = re.findall(pattern, result_data["judge"].replace("*", ""))
        while len(matches) == 0:
            print(len(result_list))
            input_msg = base_input_msg.replace(
                '[ANSWER]', result_data["lalm_answer"]
            ).replace(
                "[SENTENCE]", result_data["detail"]
            )
            ref, out_msg = openai_tool.get_respons(input_msg, model='gpt-4o')
            # 去除加粗
            out_msg = out_msg.replace("*", "")
            matches = re.findall(pattern, out_msg)
            if len(matches) != 0:
                result_data["judge"] = out_msg
            print(out_msg)
        score = matches[-1]  # 最后的是经过深思熟路的结果
        if score[-1] == ".":
            score = score[:-1]
        score = float(score)
        result_data["score"] = score
        result_list.append(score)
        with open(
                result_path.replace(
                    "gpt_judge", "gpt_judge_count"),
                'w') as f:
            json.dump(result_datas, f)

    result = np.mean(np.array(result_list))

    with open(
            result_path.replace(
                "gpt_judge", "gpt_judge_%s" % result).replace(
                "gpt_judge_count", "gpt_judge_%s" % result),
            'w') as f:
        json.dump(result_datas, f)


if __name__ == '__main__':
    for result_path in [
        "Point to the output file provided in gpt_judge mode.",
        "Such As: Q_Voice_Detective_002_s4_gpt_judge.json"
    ]:
        judge_voice_detective(result_path)
    for result_path in [
        "Point to the output file provided in gpt_judge mode.",
        "Such As: Q_Pron_Coach_001_s4_no_judge.json"
    ]:
        judge_spoken_english_coach(result_path)
    for result_path in [
        "Point to the output file provided in gpt_judge mode.",
        "Such As: Q_Pron_Coach_001_s4_no_judge.json",
    ]:
        judge_emotion_translate(result_path)
    # pass
