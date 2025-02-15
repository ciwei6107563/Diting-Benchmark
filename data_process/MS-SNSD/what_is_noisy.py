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
    json_out_dir = "~/speech_data/speech_wav/MS-SNSD"
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)

directory = "~/speech_data/speech_wav/MS-SNSD/MS-SNSD-master/synthesize_data"
all_list = list()
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".wav"):
            if "NoisySpeech_training" not in root:
                continue
            sample = dict(
                voice_absolute_path=osp.join(root, file),
                question="What is the ambient noise of this audio segment? Please choose from the ['Babble', 'CopyMachine', 'Neighbor', 'ShuttingDoor', 'AirportAnnouncements', 'Munching', 'Typing', 'AirConditioner', 'VacuumCleaner'] options?",
                answer=osp.basename(osp.dirname(root)),
                discript="",
            )
            all_list.append(sample)


if __name__ == '__main__':
    dump_json(json_filename="Q_%s.json" % "What Is Noise".replace(" ", "_"),
              dump_data=all_list)

    pass
