import jiwer
from .normalizers import EnglishTextNormalizer
import re

normalizer = EnglishTextNormalizer()


def get_wer(reference, hypothesis):
    """
    Calculate the Word Error Rate (WER) between a reference and a hypothesis.

    Args:
        reference (str): The reference text.
        hypothesis (str): The hypothesis text.

    Returns:
        float: The Word Error Rate (WER).
    """
    reference = normalizer(reference)
    hypothesis = normalizer(hypothesis)
    return jiwer.wer(reference, hypothesis)


def capitalize(s):
    s = s.capitalize()
    s = s.replace(" i ", "I")
    return s


def extract_answer(text):
    start_index = text.find("says:") + len("says:")
    extracted_text = text[start_index:].strip()

    return extracted_text


def judge(reference, answer):
    hypothesis = extract_answer(answer)
    return get_wer(reference, hypothesis)


def judge_speechGPT(reference, answer):
    return get_wer(reference, answer)


def judge_wer_find(reference, answer):
    find_list = [
        "In the audio, the person says",
        "The audio says:",
        "The person in the audio says:",
        "The original content of this audio is:",
        "The spoken content in the audio is: ",
        "The audio states:",
        "The audio segment says:",
        "The person says in English:",
        "The sentence",
        "This passage states:",
        "is said in this audio segment.",
        "The word",
        "in this audio segment.",
        "The person says in French:",
        "The lyrics are",
        "The phrase spoken in the audio is:",
        "The phrase spoken in the audio is",
        "The words uttered in the audio are:",
        "The speech in the audio is in French, saying:",
        "The speech in the audio segment is:",
        "The speech in the audio segment is",
        "The speech content is",
        "The speech in the audio is:",
        "The speech in the audio is",
        "The complete transcription of the audio is:",
        "The transcription of the audio is:",
        "The phrase said in the audio is",
        "The first speaker in the audio says",
        "The person speaking says:",
        "The person speaking says in English:",
        "The audio segment says in English:",
        "The person says:",
        "The person in the audio says",
        "The person says",
        "The sentence spoken in the audio is",
        "The transcript states",
        "The transcription of the speech is",
        "The person in the speech says",
        "The person in the speech said",
        "The transcription of the speech is",
        "The speaker said",
        "The content spoken in the audio is",
        "The person in the audio said",
        "The jailer replied gloomily",
        "The person said",
        "The speech says",
        "The person whispered",
        "The woman said",
        "The man said",
        "The person in the audio is saying",
        "In the audio, the person thinks to themselves",
        "The person in the audio thought",
        "The person thinks to themselves",
        "The person in the audio thought",
        "The man says:",
        "The speaker says",
        "</s>",
        "<s>",
    ]
    should_print = True
    for sign_str in find_list:
        # start_index = answer.find(sign_str) + len(sign_str)
        # extracted_text = answer[start_index:].strip()
        if sign_str in answer:
            should_print = False
            answer = answer.replace(sign_str, "")
    wer_out = get_wer(reference, answer)
    if should_print and wer_out > 0.05:
        print("**********")
        print(answer)
        print(reference)
    return wer_out


def judge_chinese_wer(reference, answer):
    hypothesis = extract_answer(answer)
    hypothesis = ' '.join(hypothesis)
    reference = ' '.join(reference)
    return get_wer(reference, hypothesis)


def judge__wer(reference, answer):
    import re
    # 使用正则表达式提取双引号之间的内容
    matches = re.findall(r": '(.*?)\.'", answer)
    print(matches)
    if len(matches) > 0:
        return get_wer(reference, matches[0])
    else:
        matches = re.findall(r":'(.*?)\.'", answer)
        if len(matches) > 0:
            return get_wer(reference, matches[0])
        else:
            matches = re.findall(r":'(.*?)\?'", answer)
            if len(matches) > 0:
                return get_wer(reference, matches[0])
            else:
                matches = re.findall(r": '(.*?)\?'", answer)
                if len(matches) > 0:
                    return get_wer(reference, matches[0])
                else:
                    if "says:" in answer:
                        start_index = answer.find("says:") + len("says:")
                        extracted_text = answer[start_index:].strip()
                        return get_wer(reference, extracted_text)
                    else:
                        return get_wer(reference, answer)
if __name__ == "__main__":
    reference = "Behold a ship was making for the island through the dashing sea and crashing waves"
    # print(capitalize("BEHOLD A SHIP WAS MAKING FOR THE ISLAND THROUGH THE DASHING SEA AND CLASHING WAVES"))
    hypothesis = "BEHOLD A SHIP WAS MAKING FOR THE ISLAND THROUGH THE DASHING SEA AND CLASHING WAVES."
    # hypothesis = reference
    wer = get_wer(reference, hypothesis)
    print(f"WER: {wer}")
