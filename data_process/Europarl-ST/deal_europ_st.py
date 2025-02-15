import os
import re
import os.path as osp
import json

import librosa
import soundfile as sf

tag2whole_name = dict(
    de="German",
    en="English",
    fr="French",
    es="Spanish",
    it="Italian",
)
tag_count = dict(
    de=0,
    en=0,
    fr=0,
    es=0,
    it=0,
)
tags = ["de", "en", "es", "fr", "it"]

def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "/mnt/user/bufan/speech_data/speech_wav/Europarl-ST"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)

def get_language(file_dir):
    # English (En), German (De), French (Fr) and Spanish (Es)
    # 定义可能的标签列表

    # 使用正则表达式查找这些标签
    for tag in tags:
        if re.search(tag, file_dir):
            return tag
    # 如果没有找到任何标签，则返回 None
    return None


# 指定要遍历的文件夹路径
folder_path = "/mnt/user/bufan/speech_data/speech_wav/Europarl-ST"  # 请替换为你的文件夹路径
out_dir = "/mnt/user/bufan/speech_data/speech_wav/Europarl-ST/build"
os.makedirs(out_dir,exist_ok=True)

all_list = list()

# 遍历文件夹中的所有文件和文件夹
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.m4a'):
            language_tag = get_language(root)
            if language_tag is None:
                continue
            tag_count[language_tag] = tag_count[language_tag]+1
            if tag_count[language_tag]>500:
                tags.remove(language_tag)
            # 构建完整的文件路径
            file_path = os.path.join(root, file)
            output_file = osp.join(out_dir,file[:-4]+language_tag+".wav")
            # 读取音频文件
            y, sr = librosa.load(file_path, sr=None, duration=30)  # 读取前30秒
            # 保存为wav文件
            sf.write(output_file, y, sr)
            # 将完整的文件路径添加到m4a_files列表中
            # m4a_files.append(file_path)
            sample = dict(
                voice_absolute_path=output_file,
                question="What language is spoken in this audio segment?",
                answer=tag2whole_name[language_tag],
                discript="",
            )
            all_list.append(sample)


if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "What language is".replace(" ","_"),
              dump_data=all_list)
    pass
