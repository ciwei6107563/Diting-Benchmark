import json
import os
import os.path as osp
import shutil

import pandas as pd
from pydub import AudioSegment

out_dir = "YOURDIR/jamendolyrics-master/build"
os.makedirs(out_dir, exist_ok=True)
count_dict = {
    'French': 0,
    'German': 0,
    'English': 0,
    'Spanish': 0
}


def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "YOURDIR/jamendolyrics-master"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


all_list = list()
lang_df = pd.read_csv("YOURDIR/jamendolyrics-master/JamendoLyrics.csv")


def deal_single_mp3(csv_filepath, mp3_filepath):
    mp3_filename = osp.basename(mp3_filepath)
    lang = str(lang_df[lang_df["Filepath"] == mp3_filename]["Language"].iloc[0])
    # 加载时间节点文件
    df = pd.read_csv(csv_filepath)
    # 加载MP3文件
    audio = AudioSegment.from_mp3(mp3_filepath)
    # 初始化一个空列表来存储文件内容
    wav_count = 0
    # 打开文件并读取内容
    for i in range(len(df)):
        begin_time = df.iloc[i, 0]
        end_time = df.iloc[i, 1]
        extracted_audio = audio[int(begin_time * 1000):int(end_time * 1000)]

        # 存储目标文件
        extracted_audio = extracted_audio.set_frame_rate(16000)
        extracted_audio = extracted_audio.set_channels(1)
        out_path = osp.join(
            out_dir,
            osp.basename(mp3_filepath).replace(
                ".mp3",
                "_" + str(wav_count).zfill(2) + ".wav"
            )
        )
        out_path = out_path.replace("#", "")
        extracted_audio.export(out_path, format="wav")

        sample = dict(
            voice_absolute_path=out_path,
            question="Please transcribe the lyrics of this audio segment.Please answer with: The lyrics is: xxxx",
            answer=str(df.iloc[i, 2]).strip(),
            discript="",
        )
        all_list.append(sample)
        count_dict[lang] = count_dict[lang]+1
        wav_count += 1


# 指定文件夹路径
folder_path = 'YOURDIR/jamendolyrics-master/annotations/lines'  # 请将这里的路径替换为您的文件夹路径
mp3_dir = "YOURDIR/jamendolyrics-master/mp3"
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # 确保是txt文件
        csv_filepath = os.path.join(folder_path, filename)
        mp3_filepath = osp.join(
            mp3_dir,
            osp.basename(csv_filepath).replace(".csv", ".mp3"),
        )
        deal_single_mp3(csv_filepath, mp3_filepath)

if __name__ == '__main__':
    print(count_dict)
    dump_json(json_filename="Q_%s.json" % "Song ASR".replace(" ", "_"),
              dump_data=all_list)
