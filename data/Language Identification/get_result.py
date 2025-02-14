import json
file_path = r"C:\Users\23225\PycharmProjects\SpeechDataPreprocess\gpt4O_all\Language Identification\Q_What_language_is_all_data.json"
with open(file_path,"r") as f:
    datas = json.load(f)

result_list = list()
for data in datas:
    result_path = data["voice_relative_path"].replace(".wav","_gpt4o_answer.json")
    print(result_path)
    with open(result_path,"r",encoding="utf-8") as f:
        content = f.read()  # 读取整个文件内容
        result = json.loads(content)
        if "transcript" in result["gpt4o_reply"].keys():
            lalm_answer = result["gpt4o_reply"]["transcript"]
        elif "text" in result["gpt4o_reply"].keys():
            lalm_answer = result["gpt4o_reply"]["text"]
        else:
            raise NotImplementedError
    result_list.append(
        {"lalm_answer": lalm_answer,
         "question": data["question"],
         "label_answer": data["answer"],
         "voice_absolute_path": data["voice_absolute_path"],
         "detail": "",
         "judge": None
         }
    )
with open("Language_Identification_4o_result.json", "w") as f:
    json.dump(result_list,f)
if __name__ == '__main__':
    pass
