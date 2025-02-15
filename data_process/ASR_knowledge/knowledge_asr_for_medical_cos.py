import json
import os
import os.path as osp

import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav


medical_terms = {
    "Left_Ventricle": "左心室",  # Left ventricle of the heart
    "Biceps_Brachii": "肱二头肌",  # Biceps muscle of the arm
    "Hip_Joint": "髋关节",  # Joint connecting the thigh bone to the pelvis
    "Thyroid_Gland": "甲状腺",  # Gland located in the neck that produces thyroid hormones
    "Retina": "视网膜",  # Layer of tissue at the back of the eye that is responsible for vision
    "Red_Bone_Marrow": "红骨髓",  # Marrow in bones that produces blood cells
    "Spleen": "脾脏",  # Organ that filters blood and recycles old red blood cells
    "Adrenal_Gland": "肾上腺",  # Glands above the kidneys that produce stress hormones
    "Sacrum": "骶骨",  # Triangular bone at the base of the spine
    "Cerebellum": "小脑",  # Part of the brain involved in coordination and balance
    "Pons": "脑桥",  # Part of the brainstem that connects the cerebrum and cerebellum
    "Fibula": "腓骨",  # Smaller of the two bones in the lower leg
    "Pancreas": "胰腺",  # Gland behind the stomach that secretes digestive enzymes and hormones
    "Atrium": "心房",  # Upper chambers of the heart
    "Ovaries": "卵巢",  # Female reproductive organs that produce eggs
    "Glomerulus": "肾小球",  # Tiny structures in the kidney that filter blood
    "Intestinal_Mucosa": "肠黏膜",  # Mucous membrane lining the intestines
    "Adrenal_Cortex": "肾上腺皮质",  # Outer part of the adrenal gland that produces steroid hormones
    "Prostate_Gland": "前列腺",  # Gland in males that produces seminal fluid
    "Abdominal_Aorta": "腹主动脉",  # Largest artery in the abdomen
    "Corpus_Callosum": "束状膝",  # Large bundle of fibers connecting the two hemispheres of the brain
    "Rectum": "直肠",  # Lower part of the large intestine
    "Talus": "距骨",  # Bone that connects the leg and foot
    "Deltoid_Muscle": "三角肌",  # Large muscle on the shoulder and upper arm
    "Oblique_Muscle": "斜角肌",  # Muscles on the side of the neck
    "Dura_Mater": "硬脑膜",  # Tough membrane covering the brain and spinal cord
    "Ilium": "髂骨",  # Upper part of the hip bone
    "Cochlea": "耳蜗",  # Part of the inner ear involved in hearing
    "Ribs": "肋骨",  # Bones that protect the thoracic cavity organs
    "Capillary": "毛细血管",  # Tiny blood vessels that connect arteries and veins
    "Thyroid_Cartilage": "甲状腺软骨",  # Cartilage in the neck that forms the Adam's apple
    "Tibia": "胫骨",  # Larger of the two bones in the lower leg
    "Hyoid_Bone": "舌骨",  # U-shaped bone in the neck
    "Islets_of_Langerhans": "胰岛",  # Groups of cells in the pancreas that produce insulin
    "Cranial_Nerves": "颅神经",  # Nerves that emerge directly from the brain
    "Heart_Valves": "心脏瓣膜",  # Structures that prevent backflow of blood in the heart
    "Lumbar_Spine": "腰椎",  # Lower section of the vertebral column
    "Carpal_Bones": "腕骨",  # Small bones that make up the wrist
    "Pelvic_Floor": "盆底",  # Muscles and ligaments supporting pelvic organs
    "Thymus_Gland": "胸腺",  # Gland in the chest that plays a role in immune function
    "Vocal_Cords": "声带",  # Folds in the larynx that vibrate to produce sound
    "Cerebral_Cortex": "大脑皮层",  # Outer layer of the brain involved in thought and sensation
    "Gastric_Mucosa": "胃黏膜",  # Mucous membrane lining the stomach
    "Optic_Nerve": "视神经",  # Nerve that transmits visual information from the eye to the brain
    "Liver_Lobes": "肝叶",  # Sections of the liver
    "Bronchial_Tubes": "支气管",  # Tubes that carry air into the lungs
    "Achilles_Tendon": "跟腱",  # Strong band of tissue that connects the calf muscles to the heel
    "Cornea": "角膜",  # Transparent front part of the eye
    "Thyroid_Lobes": "甲状腺叶",  # Lobes of the thyroid gland
    "Mandible": "下颌骨",  # Lower jawbone
    "Scapula": "肩胛骨",  # Bone on the shoulder blade
    "Lymph_Nodes": "淋巴结",  # Part of the lymphatic system that filters lymph
    "Pituitary_Gland": "垂体",  # Small gland at the base of the brain that controls other glands
    "Ventricles_of_the_Brain": "脑室",  # Cavity in the brain filled with cerebrospinal fluid
    "Frontal_Lobe": "额叶",  # Front part of the brain involved in decision making and problem solving
    "Parathyroid_Glands": "甲状旁腺",  # Glands near the thyroid that control calcium levels
    "Cervical_Spine": "颈椎",  # Upper part of the spine
    "White_Blood_Cells": "白细胞",  # Cells that fight infection as part of the immune system
    "Cerebrospinal_Fluid": "脑脊液",  # Fluid surrounding the brain and spinal cord
    "Sigmoid_Colon": "乙状结肠",  # Lower part of the large intestine
    "Appendix": "阑尾",  # Small organ attached to the large intestine
    "Bile_Duct": "胆管",  # Tube that carries bile from the liver to the small intestine
}




out_json_path = ""
all_list = list()
file_dir = "~/speech_data/speech_wav/ASR_knowledge"
build_base = "build_medical_cos"
os.makedirs(file_dir, exist_ok=True)

# Load TTS Model
cosyvoice = CosyVoice('pretrained_models/CosyVoice-300M')


def dump_json(json_filename, dump_data):
    """
    存储json
    :param json_filename:
    :param dump_data:
    :return:
    """
    json_out_dir = file_dir
    with open(osp.join(json_out_dir, json_filename), 'w') as f:
        json.dump(dump_data, f)


template_list = [
    "此处为[ORGAN]，大家仔细看。",
    "大家请看，[ORGAN]就在这里。",
    "我们现在看到的是[ORGAN]，它就是这个样子的。",
    "我们正在观察的是[ORGAN]，请大家看仔细。",
]


def deal_tts(sentence, file_name, label_word):
    # 生成输出位置
    out_path = osp.join(file_dir, build_base, file_name)
    os.makedirs(osp.dirname(out_path), exist_ok=True)

    # 进行语音合成和存储
    prompt_speech_16k = load_wav('zero_shot_prompt.wav', 16000)
    output = cosyvoice.inference_zero_shot(sentence, '希望你以后能够做的比我还好呦。', prompt_speech_16k)
    torchaudio.save(out_path, output['tts_speech'], 16000)

    # 存储这个sample
    sample = dict(
        voice_absolute_path=out_path,
        question="""What does the person say?please answer with " The person says: xxxx".""",
        answer=label_word,
        discript=sentence,
    )
    all_list.append(sample)


for i, template in enumerate(template_list):
    for specific_term_en, specific_term_ch in medical_terms.items():
        specific_term_en = specific_term_en.replace(" ", "_")
        new_sentence = template.replace("[ORGAN]", specific_term_ch)
        deal_tts(new_sentence, "%s/%d.wav" % (specific_term_en, i+1), specific_term_ch)
        dump_json(json_filename="Q_%s.json" % "Speech ASR Knowledge for Medical cos".replace(" ", "_"),
                  dump_data=all_list)

if __name__ == '__main__':
    print(len(all_list))
    dump_json(json_filename="Q_%s.json" % "Speech ASR Knowledge for Medical cos".replace(" ", "_"),
              dump_data=all_list)
    pass
