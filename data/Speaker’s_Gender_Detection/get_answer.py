import json
import os.path as osp
file_path = r"C:\Users\23225\PycharmProjects\SpeechDataPreprocess\gpt4O_all\Singing_Detection\Q_Is_singing_filter.json"
with open(file_path, "r") as f:
    datas = json.load(f)

import random

# 定义一个列表
my_list = ['No.', 'No, there is no singing in this audio clip.', 'No, there is no singing in this audio clip.']

random.choice(my_list)

for data in datas:
    print(data["voice_relative_path"])
    out_filepath = data["voice_relative_path"].split(".wav")[0] + "_gpt4o_answer.json"
    out_dict = dict(
        {
            "voice_relative_path": osp.abspath(data["voice_relative_path"]),
            "gpt4o_reply": {
                "type": "audio",
                "transcript": random.choice(my_list)
            }
        }
    )
    with open(out_filepath,"w") as f:
        json.dump(out_dict,f)

if __name__ == '__main__':
    pass
