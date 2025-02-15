import pandas as pd
"""
,uuid,datetime,cough_detected,latitude,longitude,age,gender,respiratory_condition,fever_muscle_pain,status,status_SSL,
quality_1,{good, ok, poor, no_cough}语音的质量
cough_type_1,{wet, dry, unknown} 干性咳嗽和湿性咳嗽
dyspnea_1,bool 可听见的呼吸困难。
wheezing_1,bool 可听见的喘息声。
stridor_1,bool 可听见的刺耳声。
choking_1,bool 声音哽咽。
congestion_1,bool 可听见的鼻塞
nothing_1,bool 没有什么值得注意的事情
diagnosis_1,{upper_infection, lower_infection, obstructive_disease, COVID-19, healthy_cough}专家对于疾病种类的印象

severity_1 pseudocough, mild, severe, unknown  专家对于严重程度的印象
"""
csv_path = r"C:\Users\23225\PycharmProjects\SpeechDataPreprocess\coughVID\metadata_compiled.csv"
label_df = pd.read_csv(csv_path,sep=",")

pd.isna(label_df.iloc[1, 0])
print()

print(label_df.head())
if __name__ == '__main__':
    pass
