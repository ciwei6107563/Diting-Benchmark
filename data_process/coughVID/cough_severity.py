import glob
import json
import os
import os.path as osp

import pandas as pd
from pydub import AudioSegment

out_dir = "~/dataset/CoughVID/build_severity"

os.makedirs(out_dir, exist_ok=True)
json_out_dir = "~/dataset/CoughVID"

get_count=170
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
base_dir = "~/dataset/CoughVID/coughvid_20211012"
# 遍历文件夹中的所有文件
all_list = list()
wet_filepath = './severity/four_non_nan_mild.csv'  # 替换为你的 CSV 文件路径
wet_df = pd.read_csv(wet_filepath)
wet_uuids = wet_df['uuid'].tolist()
wet_filepath2 = "./severity/one_non_nan_mild.csv"
wet_df = pd.read_csv(wet_filepath2)
wet_uuids.extend(wet_df['uuid'][:get_count-len(wet_uuids)].tolist())

for uuid in wet_uuids:
    matched_files = [f for f in glob.glob(osp.join(base_dir, uuid+"*")) if not f.endswith('.json')]
    if len(matched_files) == 1:
        file_path = matched_files[0]
        output_file = osp.join(out_dir, uuid+".wav")

        # 转化为16000
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)
        audio.export(output_file, format="wav")  # 你可以根据需要更改格式

        sample = dict(
            voice_absolute_path=output_file,
            question="Please help me assess the severity of the cough in the audio segment. Choose from 'pseudocough', 'mild', or 'severe'.",
            answer="mild",
            discript="",
        )
        all_list.append(sample)
    else:
        continue

dry_filepath = './severity/four_non_nan_pseudocough.csv'
dry_df = pd.read_csv(dry_filepath)
dry_uuids = dry_df['uuid'].tolist()
dry_filepath2 = "./severity/one_non_nan_pseudocough.csv"
dry_df = pd.read_csv(dry_filepath2)
dry_uuids.extend(dry_df['uuid'][:get_count-len(dry_uuids)].tolist())

for uuid in dry_uuids:
    matched_files = [f for f in glob.glob(osp.join(base_dir, uuid+"*")) if not f.endswith('.json')]
    if len(matched_files) == 1:
        file_path = matched_files[0]
        output_file = osp.join(out_dir, uuid+".wav")

        # 转化为16000
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)
        audio.export(output_file, format="wav")  # 你可以根据需要更改格式

        sample = dict(
            voice_absolute_path=output_file,
            question="Please help me assess the severity of the cough in the audio segment. Choose from 'pseudocough', 'mild', or 'severe'.",
            answer="pseudocough",
            discript="",
        )
        all_list.append(sample)
    else:
        continue

dry_filepath = './severity/four_non_nan_severe.csv'
dry_df = pd.read_csv(dry_filepath)
dry_uuids = dry_df['uuid'].tolist()
dry_filepath2 = "./severity/one_non_nan_severe.csv"
dry_df = pd.read_csv(dry_filepath2)
dry_uuids.extend(dry_df['uuid'][:get_count-len(dry_uuids)].tolist())

for uuid in dry_uuids:
    matched_files = [f for f in glob.glob(osp.join(base_dir, uuid+"*")) if not f.endswith('.json')]
    if len(matched_files) == 1:
        file_path = matched_files[0]
        output_file = osp.join(out_dir, uuid+".wav")

        # 转化为16000
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)
        audio.export(output_file, format="wav")  # 你可以根据需要更改格式

        sample = dict(
            voice_absolute_path=output_file,
            question="Please help me assess the severity of the cough in the audio segment. Choose from 'pseudocough', 'mild', or 'severe'.",
            answer="severe",
            discript="",
        )
        all_list.append(sample)
    else:
        continue


if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "COUGH SEVERITY".replace(" ", "_"),
              dump_data=all_list)