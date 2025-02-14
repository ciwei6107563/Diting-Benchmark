import json
import os.path as osp
file_path = r"C:\Users\23225\PycharmProjects\SpeechDataPreprocess\gpt4O_all\Language Identification\Q_What_language_is_all_data.json"
out_path = file_path.replace("all_data","filter")

with open(file_path,"r") as f:
    datas = json.load(f)

new_list = list()
for data in datas:
    file_path = data["voice_relative_path"]
    answer_path = file_path.replace(".wav","_gpt4o_answer.json")
    # print(answer_path)
    if not osp.exists(answer_path):
        new_list.append(data)
with open(out_path, "w") as f:
    json.dump(new_list,f)

print(len(new_list))

if __name__ == '__main__':
    pass
