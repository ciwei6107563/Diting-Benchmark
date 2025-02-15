import os
import json
import os.path as osp


def find_json_files(directory):
    """
    找出指定目录及子目录下所有不以"_check_unk.json"结尾的JSON文件。

    参数：
    - directory: 根目录路径

    返回：
    - json_files: 符合条件的JSON文件路径列表
    """
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("_check_unk.json"):
                json_files.append(os.path.join(root, file))
    return json_files


def dont_has_large_gap(intervals):
    # print(intervals)
    for i in range(len(intervals)):
        if intervals[i][1] - intervals[i][0] > 0.6:
            return False
    return True


def deal_data(directory):
    new_list = list()
    sum_len = 500
    for json_filepath in find_json_files(directory):
        # print(json_filepath)
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for single_data in data:
            find_pauses = single_data.get("find_pauses", [])
            content = single_data.get("Content", "")
            if len(find_pauses) == 0:
                sample = dict(
                    voice_absolute_path=single_data["relative_path"],
                    question="Please determine if there are noticeable pauses in this audio. Answer with 'yes' or 'no.'",
                    answer="no",
                    discript=f"The pauses is {str(find_pauses)}, and the context is {content}",
                )
                new_list.append(sample)
                if len(new_list) >= sum_len:
                    return new_list

# 读取 JSON 文件
def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "~/speech_data/TED-LIUM"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    directory = "~/speech_data/TED-LIUM/TEDLIUM_split"
    print(directory)
    new_list = deal_data(directory)
    dump_json(json_filename="Q_%s.json" % "Pauses Detection 1".replace(" ", "_"),
              dump_data=new_list)
    pass