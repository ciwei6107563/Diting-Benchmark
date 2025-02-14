import os
import random
from collections import defaultdict
import shutil
import json
import os.path as osp
random.seed(42)

old_base_dir = "/mnt/user/bufan/speech_data/speech_wav/VCTK/VCTK-Corpus"
new_base_dir = "/mnt/user/bufan/speech_data/speech_wav/VCTK/all_data"
old_json_path = "/mnt/user/bufan/speech_data/speech_wav/VCTK/Q_Gender_Detection_16000.json"
new_json_path = "/mnt/user/bufan/speech_data/speech_wav/VCTK/Q_Gender_Detection_all_data.json"

with open(old_json_path, "r") as f:
    datas = json.load(f)


# 创建一个新的列表用于存储每个类别中抽取的数据
new_list = datas

for data in new_list:
    source_file = data["voice_absolute_path"]
    to_dir = osp.dirname(source_file.replace(old_base_dir, new_base_dir))
    os.makedirs(to_dir, exist_ok=True)
    data["voice_relative_path"] = source_file.replace(old_base_dir, ".")

    shutil.copy(source_file, to_dir)

with open(new_json_path, "w") as f:
    json.dump(new_list, f)

if __name__ == '__main__':
    pass
