import pandas as pd


def filter_quality(filepath,out_filepath):
    # 读取CSV文件
    df = pd.read_csv(filepath)
    # 筛选至少有三列专家判定为 'wet' 的行
    # axis=1 表示按行进行判断
    filtered_df = df[(df[['quality_1', 'quality_2', 'quality_3', 'quality_4']] == 'good').sum(axis=1) >= 1]

    # 将筛选结果保存为新的CSV文件
    filtered_df.to_csv(out_filepath, index=False)


# filepath = "filtered_dry_output.csv"
# out_filepath = "filtered_dry_output_good.csv"

filepath = "filtered_wet_output.csv"
out_filepath = "filtered_wet_output_good.csv"
filter_quality(filepath, out_filepath)

# one_non_nan.csv

filepath = "one_non_nan.csv"
out_filepath = "one_non_nan_good.csv"
filter_quality(filepath, out_filepath)
if __name__ == '__main__':
    pass
