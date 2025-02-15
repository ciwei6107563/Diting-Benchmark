import json
import os
from pydub import AudioSegment
from pydub.silence import detect_silence

audio_root = "~/speech_data/TED-LIUM"  # 音频文件的根目录


# 停顿检测函数
def find_pauses(audio_path, silence_thresh=-40, min_silence_len=500):
    try:
        audio = AudioSegment.from_file(audio_path)
        pauses = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        return [(start / 1000.0, end / 1000.0) for start, end in pauses]
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return []


# 处理 JSON 文件
def process_json(input_json_path):
    output_json_path = input_json_path.replace(".json", "_check_unk.json")
    # 加载 JSON 数据
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 初始化输出列表
    result = []

    for item in data:
        content = item.get("Content", "")
        relative_path = item.get("relative_path", "")
        audio_path = os.path.join(audio_root, relative_path)

        # 检测 `<unk>` 是否既不在开头也不在结尾
        if "<unk>" in content and not (content.startswith("<unk>") or content.endswith("<unk> ")):
            print(f"Processing: {relative_path}")
            # 检测停顿
            pauses = find_pauses(audio_path)

            # 如果检测到了停顿，将其加入新的属性
            if pauses:
                item["find_pauses"] = pauses

            # 将结果添加到新的列表
            result.append(item)

    # 保存结果到新 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Processed data saved to {output_json_path}")


def find_json_files(directory):
    """
    找出指定目录及子目录下所有不以"_check_unk.json"结尾的JSON文件。

    参数：
    - directory: 根目录路径

    返回：
    - json_files: 符合条件的JSON文件路径列表
    """
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json") and not file.endswith("_check_unk.json"):
                json_files.append(os.path.join(root, file))
    return json_files




if __name__ == '__main__':
    directory = "~/speech_data/TED-LIUM/TEDLIUM_split"
    json_files = find_json_files(directory)
    for json_filepath in json_files:
        process_json(json_filepath)
    pass
