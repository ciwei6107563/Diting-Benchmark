import json
import os
import os.path as osp

import numpy as np
import pandas as pd
import pyworld as pw
import soundfile as sf


def find_range(wav_path, fs=16000, frame_period=5.0):
    # 加载音频文件
    x, sr = sf.read(wav_path)

    # 使用pyworld提取基频
    _f0, t = pw.dio(x, fs, frame_period=frame_period)  # Raw pitch track
    f0 = pw.stonemask(x, _f0, t, fs)  # Refine pitch track
    pitch_values_filtered = f0[f0 != 0]
    for m, n in [(80, 150), (180, 250)]:
        # 计算在 m 和 n 之间的元素比例
        percentage = np.mean((pitch_values_filtered >= m) & (pitch_values_filtered <= n))
        if m == 80:
            if percentage > 0.9:
                return (m, n), percentage
            continue
        if percentage > 0.72:
            return (m, n), percentage
    return None, None


def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = "~/speech_wav/SpeechAccentArchive"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


# 读取CSV文件
df = pd.read_csv('~/speech_wav/SpeechAccentArchive/speakers_all.csv')  # 请将 'your_file.csv' 替换为您的实际文件路径

# 提取 "filename" 和 "age" 列
filenames = df['filename'].tolist()
ages = df['age'].tolist()
begin_ages = df["age_onset"].tolist()
sexs = df["sex"].tolist()
native_languages = df["native_language"].tolist()
birthplaces = df["birthplace"].tolist()
# native_language,sex,birthplace
all_list = list()

wav16000_dir = "/~/speech_wav/SpeechAccentArchive/build"
build_f0 = "~/speech_wav/SpeechAccentArchive/build_f0"

count_dict = dict()
# 打印结果
for filename, age, begin_age, sex, native_language, birthplace in zip(
        filenames, ages, begin_ages, sexs, native_languages, birthplaces
):
    wav_path = osp.join(wav16000_dir, filename + ".wav")
    if not os.path.exists(wav_path):
        continue
    f0_range, percentage = find_range(wav_path)
    print(f0_range, percentage)
    if f0_range is not None:
        sample = dict(
            voice_absolute_path=wav_path,
            question="In the following audio segment, into which range does more than 70% of the fundamental frequency content fall? Please choose from the following two ranges: (80, 150) Hz and (180, 250) Hz.",
            answer=str(f0_range),
            discript="age:%d,gender:%s,The percentage of the content within the interval %s is %f" %
                     (age, sex, str(f0_range), percentage),
        )
        if str(f0_range) not in count_dict.keys():
            count_dict[str(f0_range)] = 1
        else:
            count_dict[str(f0_range)] += 1
        all_list.append(sample)
    dump_json(
        json_filename="Q_%s.json" % "F0 Detective".replace(" ", "_"),
        dump_data=all_list
    )

if __name__ == '__main__':
    print(count_dict)
    dump_json(json_filename="Q_%s.json" % "F0 Detective end".replace(" ", "_"),
              dump_data=all_list)
