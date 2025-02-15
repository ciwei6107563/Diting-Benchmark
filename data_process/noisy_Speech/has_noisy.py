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
    json_out_dir = "~/speech_wav/VCTK"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)

directory = "~/speech_wav/Noisy-speech-database"
all_list = list()
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".wav"):
            sample = dict(
                voice_absolute_path=osp.join(root, file),
                question="Is there any ambient noise in this audio segment, in addition to the speaker’s voice?Please answer with “yes” or “no”",
                answer="yes" if "noisy_testset_wav" in root else "no",
                discript="",
            )
            all_list.append(sample)


if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "Has Noise".replace(" ", "_"),
              dump_data=all_list)

    pass
