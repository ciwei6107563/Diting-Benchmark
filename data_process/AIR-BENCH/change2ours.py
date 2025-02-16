import json
import os.path as osp
filepath = "~/speech_wav/AIR-Bench-Dataset/Foundation/Foundation_meta.json"
json_out_dir = "~/speech_wav/AIR-Bench-Dataset"

all_list = list()


count_dict = {
    'teens to twenties': 0,
    'thirties to fourties': 0,
    'fifties to sixties': 0,
    'seventies to eighties': 0
}

def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)

air_bench_base = "~/speech_wav/AIR-Bench-Dataset/Foundation/Speaker_Age_Prediction_common_voice_13.0_en"
with open(filepath, 'r') as file:
    datas = json.load(file)
    for data in datas:
        if data["task_name"] == "Speaker_Age_Prediction":
            sample = dict(
                voice_absolute_path=osp.join(
                    air_bench_base,
                    data["path"]
                ),
                question="Which age range do you believe best matches the speaker's voice? Please choose from the ['teens to twenties', 'thirties to fourties', 'fifties to sixties'] options?",
                answer=data["answer_gt"],
                discript="",
            )
            all_list.append(sample)
            count_dict[data["answer_gt"]] = count_dict[data["answer_gt"]] + 1


if __name__ == '__main__':
    print(count_dict)
    dump_json(json_filename="Q_%s.json" % "Age Detection".replace(" ", "_"),
              dump_data=all_list)
    pass
