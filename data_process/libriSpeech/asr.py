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
    json_out_dir = "/mnt/user/bufan/speech_data/speech_wav/LibriSpeech"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


def get_text(flac_filepath):
    txt_filename = list(filter(
        lambda filename_: filename_.endswith("txt"),
        os.listdir(osp.dirname(flac_filepath))))[0]
    txt_filepath = osp.join(osp.dirname(flac_filepath), txt_filename)

    def read_text_from_file():
        data_dict = dict()

        with open(txt_filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ', 1)  # Split the line into key and value at the first space
                if len(parts) == 2:
                    key, value = parts
                    data_dict[key] = value

        return data_dict

    filename = osp.basename(flac_filepath).split(".")[0]
    return read_text_from_file()[filename]


directory = "/mnt/user/bufan/speech_data/speech_wav/LibriSpeech/LibriSpeech"
all_list = list()
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".flac"):
            sample = dict(
                voice_absolute_path=osp.join(root, file),
                question="'What does the person say?please answer with \" The person says: xxxx\".'",
                answer=get_text(osp.join(root, file)),
                discript="",
            )
            all_list.append(sample)

if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "Speech ASR".replace(" ", "_"),
              dump_data=all_list)

    pass
