import json
import os
import os.path as osp

import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav


legal_terms = {
    "Intentional_Homicide": "故意杀人罪",  # Refers to the intentional and illegal deprivation of another person's life.
    "Negligent_Homicide": "过失杀人罪",  # Refers to causing someone's death due to negligence or carelessness.
    "Robbery": "抢劫罪",  # Refers to the act of using violence, threats, or other means to openly seize public or private property with the intent to illegally possess it.
    "Extortion": "敲诈勒索罪",  # Refers to the act of coercing someone to give up property by using threats or intimidation.
    "Fraud": "诈骗罪",  # Refers to obtaining someone else's property by means of deception or concealment of facts.
    "Infringement_of_Intellectual_Property": "侵犯知识产权罪",  # Refers to the illegal use or reproduction of another person's intellectual property, such as patents, trademarks, or copyrights.
    "Abuse_of_Power": "滥用职权罪",  # Refers to government officials abusing their power, causing significant harm to the state or public interest.
    "Bribery": "受贿罪",  # Refers to government officials illegally accepting money or goods in exchange for offering favors or benefits.
    "Abandonment": "遗弃罪",  # Refers to the intentional abandonment of a person with an obligation to support, leaving them in a destitute state.
    "Illegal_Detention": "非法拘禁罪",  # Refers to the illegal deprivation of another person's personal freedom.
    "Embezzlement": "职务侵占罪",  # Refers to the illegal appropriation of public or private property by someone entrusted with its management.
    "Perjury": "伪证罪",  # Refers to the act of deliberately making false statements in judicial proceedings.
    "Obstruction_of_Justice": "妨害公务罪",  # Refers to intentionally obstructing state officials from carrying out their duties.
    "Misappropriation_of_Public_Funds": "挪用公款罪",  # Refers to the act of illegally using public funds for private purposes.
    "Contract_Fraud": "合同诈骗罪",  # Refers to the act of fraudulently obtaining property during the signing or execution of a contract.
    "Tax_Evasion": "虚开增值税发票罪",  # Refers to illegally issuing or purchasing false value-added tax (VAT) invoices.
    "Illegal_Business_Operations": "非法经营罪",  # Refers to engaging in business activities without the proper licenses or permits.
    "Smuggling": "走私罪",  # Refers to the illegal transportation or concealment of goods or substances across borders.
    "Manufacture_or_Sale_of_Dangerous_Substances": "非法制造、买卖、运输、储存危险物质罪",  # Refers to the illegal manufacturing, sale, transport, or storage of hazardous substances.
    "Money_Laundering": "洗钱罪",  # Refers to disguising or concealing the origin of illegal funds through transactions.
    "Escape": "脱逃罪",  # Refers to a detainee or prisoner illegally escaping from custody.
    "Credit_Card_Fraud": "妨害信用卡管理罪",  # Refers to illegal use, sale, or production of fraudulent credit cards.
    "Copyright_Infringement": "侵犯著作权罪",  # Refers to illegally copying or distributing copyrighted works.
    "Illegal_Entry_into_Dwelling": "私自侵入住宅罪",  # Refers to entering someone else's home without permission.
    "Intentional_Assault": "故意伤害罪",  # Refers to intentionally causing harm to another person.
    "Prostitution_Offenses": "组织、强迫、诱导、容留、引诱卖淫罪",  # Refers to organizing, coercing, inducing, or facilitating prostitution.
    "Illegal_Collection_of_Personal_Information": "非法获取公民信息罪",  # Refers to illegally obtaining or selling personal information without consent.
}



out_json_path = ""
all_list = list()
file_dir = "~/speech_data/speech_wav/ASR_knowledge"
build_base = "build_law"
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
    "他构成了[CRIME]的既遂，法官当庭宣判。",
    "他构成了[CRIME]的未遂，法官当庭宣判。",
    "张三因[CRIME]的既遂被判处刑罚，法官当庭宣判。",
    "张三因[CRIME]的未遂被判处刑罚，法官当庭宣判。",
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
    for specific_term_en, specific_term_ch in legal_terms.items():
        specific_term_en = specific_term_en.replace(" ", "_")
        new_sentence = template.replace("[CRIME]", specific_term_ch)
        if "既遂" in template:
            specific_term_ch += "的既遂"
        elif "的未遂" in template:
            specific_term_ch += "的未遂"
        deal_tts(new_sentence, "%s/%d.wav" % (specific_term_en, i+1), specific_term_ch)
        dump_json(json_filename="Q_%s.json" % "Speech ASR Knowledge for Law_cos".replace(" ", "_"),
                  dump_data=all_list)

if __name__ == '__main__':
    print(len(all_list))
    dump_json(json_filename="Q_%s.json" % "Speech ASR Knowledge for Law_cos".replace(" ", "_"),
              dump_data=all_list)
    pass
