import pandas as pd

# 读取CSV文件
df = pd.read_csv(r'C:\Users\23225\PycharmProjects\SpeechDataPreprocess\coughVID\four_non_nan.csv')

# 筛选至少有三列专家判定为 'wet' 的行
# axis=1 表示按行进行判断
filtered_df = df[(df[['cough_type_1', 'cough_type_2', 'cough_type_3', 'cough_type_4']] == 'wet').sum(axis=1) >= 3]

# 将筛选结果保存为新的CSV文件
filtered_df.to_csv(r'C:\Users\23225\PycharmProjects\SpeechDataPreprocess\coughVID\four_non_nan_wet.csv.csv', index=False)


filtered_df = df[(df[['cough_type_1', 'cough_type_2', 'cough_type_3', 'cough_type_4']] == 'dry').sum(axis=1) >= 3]

# 将筛选结果保存为新的CSV文件
filtered_df.to_csv(r'C:\Users\23225\PycharmProjects\SpeechDataPreprocess\coughVID\four_non_nan_dry.csv.csv', index=False)


# 读取CSV文件
df = pd.read_csv(r'C:\Users\23225\PycharmProjects\SpeechDataPreprocess\coughVID\one_non_nan.csv')


nan_count = df[['cough_type_1', 'cough_type_2', 'cough_type_3', 'cough_type_4']].isna().sum(axis=1)

# 判断每一行中是否有且只有一个 'dry'
dry_count = (df[['cough_type_1', 'cough_type_2', 'cough_type_3', 'cough_type_4']] == 'dry').sum(axis=1)
wet_count = (df[['cough_type_1', 'cough_type_2', 'cough_type_3', 'cough_type_4']] == 'wet').sum(axis=1)

# 筛选出符合条件的行，即 NaN 的数量为 3，且 'dry' 的数量为 1
filtered_df_dry = df[(nan_count == 3) & (dry_count == 1)]
filtered_df_wet = df[(nan_count == 3) & (wet_count == 1)]

# 将筛选结果保存为新的CSV文件
filtered_df_dry.to_csv('filtered_dry_output.csv', index=False)
filtered_df_wet.to_csv('filtered_wet_output.csv', index=False)

if __name__ == '__main__':
    pass
