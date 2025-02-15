import pandas as pd

# 读取CSV文件
df = pd.read_csv(r'~\coughVID\metadata_compiled.csv')

# 指定要检查的列
columns_to_check = ['quality_1', 'quality_2', 'quality_3', 'quality_4']

# 过滤操作：只保留至少一个指定列的值不是NaN的行
filtered_df = df.dropna(subset=columns_to_check, how='all')

# 保存结果到新的CSV文件
filtered_df.to_csv('filtered_file.csv', index=False)

print("过滤完成，已保存新的CSV文件")

# 指定要检查的列
columns_to_check = ['quality_1', 'quality_2', 'quality_3', 'quality_4']

# 计算每行中指定列不是NaN的数量
non_nan_count = df[columns_to_check].notna().sum(axis=1)

# 过滤出有两个属性不是NaN的行
one_non_nan = df[non_nan_count == 1]

# 过滤出有两个属性不是NaN的行
two_non_nan = df[non_nan_count == 2]

# 过滤出有三个属性不是NaN的行
three_non_nan = df[non_nan_count == 3]

# 过滤出有四个属性不是NaN的行
four_non_nan = df[non_nan_count == 4]

# 保存结果到新的CSV文件
one_non_nan.to_csv('one_non_nan.csv', index=False)
two_non_nan.to_csv('two_non_nan.csv', index=False)
three_non_nan.to_csv('three_non_nan.csv', index=False)
four_non_nan.to_csv('four_non_nan.csv', index=False)

print("过滤完成，已保存符合条件的CSV文件")


if __name__ == '__main__':
    pass
