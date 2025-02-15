import os
import os.path as osp
import json
from pydub import AudioSegment

num2emo = dict({
    1: "neutral", 2: "calm", 3: "happy", 4: "sad",
    5: "angry", 6: "fearful", 7: "disgust", 8: "surprised"
})

out_dir = "/YOURDIR/RAVDESS"


def concatenate_audio_files(file1, file2, output_file):
    from pydub import AudioSegment
    from pydub.utils import mediainfo
    # 加载两个音频文件
    audio1 = AudioSegment.from_file(file1)
    audio2 = AudioSegment.from_file(file2)

    # 检查两个音频文件是否具有相同的采样率
    sample_rate1 = mediainfo(file1)['sample_rate']
    sample_rate2 = mediainfo(file2)['sample_rate']

    if sample_rate1 != sample_rate2:
        raise ValueError("The two audio files must have the same sample rate.")

    # 连接两个音频文件
    combined_audio = audio1 + audio2

    # 转化为16000采样率
    combined_audio = combined_audio.set_frame_rate(16000)

    # 导出合并后的音频文件
    combined_audio.export(output_file, format="wav")  # 你可以根据需要更改格式

    return output_file


def get_emotion(file_path):
    return num2emo[int(osp.basename(file_path).split("-")[2])]


def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    with open(osp.join(out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)




class Q_What_emotion_speech:
    def __init__(self):
        pass

    @staticmethod
    def generate_question():
        directory = 'YOURDIR/RAVDESS/speech'
        new_base_dir = 'YOURDIR/RAVDESS/new_build/speech'
        all_list = list()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    emo = get_emotion(file_path)
                    if emo == "calm":
                        continue

                    # 转化采样频率
                    new_path = file_path.replace(directory, new_base_dir)
                    os.makedirs(osp.dirname(new_path), exist_ok=True)
                    audio = AudioSegment.from_file(file_path)
                    audio = audio.set_frame_rate(16000)
                    audio.export(new_path, format="wav")

                    sample = dict(
                        voice_absolute_path=new_path,
                        question="""What emotion does this audio clip convey?Please answer by single word select from ["neutral", "happy", "sad", "angry", "fearful", "disgust","surprised"].""",
                        answer=emo,
                        discript=""
                    )
                    all_list.append(sample)
                    # 这里可以添加代码来处理每个.wav文件，例如加载或分析音频
        dump_json(json_filename="Q_%s.json" % "What_emotion_speech_new".replace(" ", "_"),
                  dump_data=all_list)


class Q_Which_emotion_strong:

    def __init__(self):
        pass

    @staticmethod
    def generate_question():
        directory = 'YOURDIR/RAVDESS/speech'
        output_dir = "YOURDIR/RAVDESS/build/strong_new"
        os.makedirs(output_dir, exist_ok=True)
        all_list = list()
        for root, dirs, files in os.walk(directory):
            for i, file in enumerate(files):
                # 检查文件扩展名是否为.wav
                if file.endswith(".wav") and file.split("-")[3] == "02":

                    # 构建完整的文件路径
                    file_path = os.path.join(root, file)

                    if get_emotion(file_path) not in ["angry", "fearful", "disgust"]:
                        continue
                    pair_path = file_path[:len(file_path) - 14] + str(1) + file_path[len(file_path) - 13:]
                    new_path = osp.join(output_dir, osp.basename(file_path))

                    sample = dict(
                        voice_absolute_path=concatenate_audio_files(file_path, pair_path, new_path) if i % 2 == 0 else
                        concatenate_audio_files(pair_path, file_path, new_path),
                        question="In this audio segment, a sentence is repeated twice. Is the emotion in the \"former\" stronger or the \"latter\" stronger? Please answer with \"former\" or \"latter.\"",
                        answer="former" if i % 2 == 0 else "latter",
                        discript=""
                    )
                    all_list.append(sample)
                    # 这里可以添加代码来处理每个.wav文件，例如加载或分析音频
        dump_json(json_filename="Q_%s.json" % "Which_emotion_strong_new".replace(" ", "_"),
                  dump_data=all_list)


class Q_is_singing:
    def __init__(self):
        pass

    @staticmethod
    def generate_question():
        all_list = list()
        directory = 'YOURDIR/RAVDESS/song'
        for root, dirs, files in os.walk(directory):
            for i, file in enumerate(files):
                # 检查文件扩展名是否为.wav
                if file.endswith(".wav"):
                    # 构建完整的文件路径
                    file_path = os.path.join(root, file)
                    # 打印文件路径或进行其他操作
                    sample = dict(
                        voice_absolute_path=osp.abspath(file_path),
                        question="Is there singing in this audio clip?Please answer by yes or no",
                        answer="yes",
                        discript=""
                    )
                    all_list.append(sample)
                    # 这里可以添加代码来处理每个.wav文件，例如加载或分析音频
        directory = 'YOURDIR/RAVDESS/speech'
        for root, dirs, files in os.walk(directory):
            for i, file in enumerate(files):
                # 检查文件扩展名是否为.wav
                if file.endswith(".wav"):
                    # 构建完整的文件路径
                    file_path = os.path.join(root, file)
                    # 打印文件路径或进行其他操作
                    sample = dict(
                        voice_absolute_path=osp.abspath(file_path),
                        question="Is there singing in this audio clip?Please answer by yes or no",
                        answer="no",
                        discript=""
                    )
                    all_list.append(sample)
                    # 这里可以添加代码来处理每个.wav文件，例如加载或分析音频
        dump_json(json_filename="Q_%s.json" % "Is_singing".replace(" ", "_"),
                  dump_data=all_list)


class Q_What_emotion_song:
    def __init__(self):
        pass

    @staticmethod
    def generate_question():
        directory = 'YOURDIR/RAVDESS/song'
        new_base_dir = 'YOURDIR/RAVDESS/new_build/song'
        all_list = list()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    emo = get_emotion(file_path)
                    if emo == "calm":
                        continue

                    # 转化采样频率
                    new_path = file_path.replace(directory, new_base_dir)
                    os.makedirs(osp.dirname(new_path), exist_ok=True)
                    audio = AudioSegment.from_file(file_path)
                    audio = audio.set_frame_rate(16000)
                    audio.export(new_path, format="wav")

                    sample = dict(
                        voice_absolute_path=new_path,
                        question=""" What emotion does this audio clip convey?Please answer by single word select from ["neutral", "happy", "sad", "angry", "fearful"].""",
                        answer=emo,
                        discript=""
                    )
                    all_list.append(sample)
                    # 这里可以添加代码来处理每个.wav文件，例如加载或分析音频
        dump_json(json_filename="Q_%s.json" % "What_emotion_song_new".replace(" ", "_"),
                  dump_data=all_list)




if __name__ == '__main__':
    Q_What_emotion_song.generate_question()
    Q_What_emotion_speech.generate_question()
    Q_Which_emotion_strong.generate_question()
    Q_is_singing.generate_question()
    pass
