import os
import os.path as osp
import json

def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "~/speech_data/LungSongs"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)
def categorize_wav_files(directory):
    # 初始化两个列表
    list1 = []
    list2 = []

    # 遍历文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为 .wav
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)

                # 判断文件名是否包含 "N,N"
                if "N,N" in file:
                    list1.append(file_path)
                else:
                    list2.append(file_path)

    return list1, list2



# 示例用法
if __name__ == "__main__":
    input_directory = "~/speech_data/LungSongs/Audio Files"
    list1, list2 = categorize_wav_files(input_directory)

    all_list = list()

    for normal_filepath in list1:
        sample = dict(
            voice_relative_path=normal_filepath.replace("~/speech_data/LungSongs/Audio Files",""),
            question="Do you think this lung breathing sound is healthy? Please answer with 'yes' or 'no'.",
            answer="yes",
            discript=f"",
        )
        all_list.append(sample)
    for un_normal_filepath in list1:
        sample = dict(
            voice_relative_path=un_normal_filepath.replace("~/speech_data/LungSongs/Audio Files",""),
            question="Do you think this lung breathing sound is healthy? Please answer with 'yes' or 'no'.",
            answer="no",
            discript=f"",
        )
        all_list.append(sample)

    # 保存筛选后的数据
    dump_json(json_filename="Q_%s.json" % "Energy Detection".replace(" ", "_"),
              dump_data=all_list)
