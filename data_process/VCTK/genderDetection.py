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
    json_out_dir = "/mnt/user/bufan/speech_data/speech_wav/VCTK"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


def parse_line(line):
    parts = line.strip().split()
    id, age, gender, nationality = parts[:4]
    location = ' '.join(parts[4:]) if len(parts) > 4 else None
    return id, age, gender, nationality, location

def read_spk_file(filename):
    speaker_dict = dict()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行
            if "AGE" in line:
                continue
            row = parse_line(line)
            speaker_dict["p"+row[0]] = dict(
                age=int(row[1]),
                gender=row[2],
                accent=row[3],
            )
    return speaker_dict

def get_speaker_gender(speaker_dict,speaker):
    label2whole = dict(
        F="female",
        M="male",
    )
    return label2whole[speaker_dict[speaker]["gender"]]



speaker_filepath = "/mnt/user/bufan/speech_data/speech_wav/VCTK/VCTK-Corpus/speaker-info.txt"
speaker_dict = read_spk_file(speaker_filepath)

base_wav_dir = "/mnt/user/bufan/speech_data/speech_wav/VCTK/VCTK-Corpus/wav48"
all_list = list()
for speaker_dir in os.listdir(base_wav_dir):
    if speaker_dir not in speaker_dict.keys():
        continue
    use_list = ['p225', 'p228', 'p229', 'p230', 'p231', 'p233', 'p234', 'p236', 'p238', 'p239', 'p240', 'p244', 'p248',
                'p249', 'p250', 'p253', 'p257', 'p261', 'p262', 'p264', 'p265', 'p266', 'p267', 'p268', 'p269', 'p276',
                'p277', 'p282', 'p283', 'p288', 'p293', 'p294', 'p295', 'p297', 'p299', 'p300', 'p301', 'p303', 'p305',
                'p306', 'p307', 'p308', 'p310', 'p312', 'p313', 'p314', 'p317', 'p226', 'p227', 'p232', 'p237', 'p241',
                'p243', 'p245', 'p246', 'p247', 'p251', 'p252', 'p254', 'p255', 'p256', 'p258', 'p259', 'p260', 'p263',
                'p270', 'p271', 'p272', 'p273', 'p274', 'p275', 'p278', 'p279', 'p281', 'p284', 'p285', 'p286', 'p287',
                'p292', 'p298', 'p302', 'p304', 'p311', 'p315', 'p316', 'p326', 'p334', 'p345', 'p347', 'p360', 'p363',
                'p364', 'p374', 'p376']

    if speaker_dir not in use_list:
        continue
    wav_files = os.listdir(osp.join(base_wav_dir, speaker_dir))
    wav_files.sort()
    for i in range(30):
        wav_filename = wav_files[i]
        wav_filepath = osp.join(base_wav_dir, speaker_dir, wav_filename)
        sample = dict(
            voice_absolute_path=wav_filepath,
            question="Is the speaker in this audio segment male or female?",
            answer=get_speaker_gender(speaker_dict,speaker_dir),
            discript="",
        )
        all_list.append(sample)

if __name__ == "__main__":
    dump_json(json_filename="Q_%s.json" % "Gender Detection".replace(" ", "_"),
              dump_data=all_list)

