import json
import os
import os.path as osp

out_dir = "/wangbenyou/bufan/speech_wav/CoughSegmentationData"
os.makedirs(out_dir, exist_ok=True)
json_out_dir = "/wangbenyou/bufan/speech_wav/CoughSegmentationData"


def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


# 指定文件夹路径
folder_path = '/wangbenyou/bufan/speech_wav/CoughSegmentationData/virufy-data/clinical/segment'  # 请将这里的路径替换为您的文件夹路径
# 遍历文件夹中的所有文件
all_list = list()
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".wav"):
            sample = dict(
                voice_absolute_path=os.path.join(root, file),
                question="Please listen to the following cough sound and determine whether the person is at risk of having a COVID-19 infection. Please answer with either 'yes' or 'no'",
                answer="yes" if "pos" in root else "no",
                discript="",
            )
            all_list.append(sample)

if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "COVID-19 Detection".replace(" ", "_"),
              dump_data=all_list)
