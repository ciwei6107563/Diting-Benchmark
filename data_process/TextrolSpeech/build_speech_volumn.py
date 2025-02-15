import json
from collections import defaultdict
import os.path as osp

change_label = dict({
    "low": "soft",
    "high": "loud"
})

change_gender_label = dict({
    "F": "female",
    "M": "male"
})


# 读取 JSON 文件
def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "~/speech_data/TextrolSpeech"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)


# 根据条件筛选数据
def filter_data(data, group_size=250):
    # 创建四个类别的分组
    groups = defaultdict(list)
    for item in data:
        gender = item.get("gender")
        energy = item.get("energy")
        if gender == "M" and energy == "high":
            groups["male_fast"].append(item)
        elif gender == "F" and energy == "high":
            groups["female_fast"].append(item)
        elif gender == "M" and energy == "low":
            groups["male_slow"].append(item)
        elif gender == "F" and energy == "low":
            groups["female_slow"].append(item)

    # 从每个分组中选择指定数量的条目
    result = []
    for key in ["male_fast", "female_fast", "male_slow", "female_slow"]:
        result.extend(groups[key][:group_size])
    new_list = list()
    for single_data in result:
        speaker_gender = single_data["gender"]
        sample = dict(
            voice_absolute_path=single_data["path"],
            question="Please determine whether the following audio clip has a loud or soft sound. Please respond with 'loud' or 'soft'.",
            answer=change_label[single_data["energy"]],
            discript=f"The speaker is {change_gender_label[speaker_gender]}",
        )
        new_list.append(sample)

    return new_list


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    input_file = '~/speech_data/TextrolSpeech/libritts.json'  # 输入 JSON 文件路径

    # 加载 JSON 数据
    data = load_json(input_file)

    # 筛选数据
    new_list = filter_data(data, group_size=250)

    # 保存筛选后的数据
    dump_json(json_filename="Q_%s.json" % "Energy Detection".replace(" ", "_"),
              dump_data=new_list)