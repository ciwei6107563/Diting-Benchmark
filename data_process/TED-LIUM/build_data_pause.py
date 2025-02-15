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
            if  file.endswith("_check_unk.json"):
                json_files.append(os.path.join(root, file))
    return json_files

def has_large_gap(intervals):
    # print(intervals)
    for i in range(len(intervals)):
        if intervals[i][1] - intervals[i][0] > 1.3:
            return True
    return False


def deal_data(directory):
    new_list = list()
    sum_len = 500
    for json_filepath in find_json_files(directory):
        # print(json_filepath)
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for single_data in data:
            content = single_data.get("Content", "")
            find_pauses = single_data.get("find_pauses", [])
            # print(find_pauses)
            if len(find_pauses)>=3 and not content.endswith("<unk> "):
                # print(find_pauses)
                if has_large_gap(find_pauses[1:-1]):
                    # print(single_data["relative_path"])
                    sample = dict(
                        voice_absolute_path=single_data["relative_path"],
                        question="Please determine if there are noticeable pauses in this audio. Answer with 'yes' or 'no.'",
                        answer="yes",
                        discript=f"The pauses is {str(find_pauses)}",
                    )
                    new_list.append(sample)
                    print(len(new_list))
                    if len(new_list)>=sum_len:
                        return new_list

# 读取 JSON 文件
def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "/home/zhiyu/speech_data/TED-LIUM"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    directory = "/home/zhiyu/speech_data/TED-LIUM/TEDLIUM_split"
    print(directory)
    new_list = deal_data(directory)
    dump_json(json_filename="Q_%s.json" % "Pauses Detection".replace(" ", "_"),
              dump_data=new_list)
    pass
