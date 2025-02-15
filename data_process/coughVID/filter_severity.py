import pandas as pd


#

def filter_quality(filepath, out_filepath, origin_type):
    # 读取CSV文件
    df = pd.read_csv(filepath)
    # 筛选至少有三列专家判定为 'wet' 的行
    # axis=1 表示按行进行判断
    filtered_df = df[(df[['severity_1', 'severity_2', 'severity_3', 'severity_4']] == origin_type).sum(axis=1) >= 3]

    # 将筛选结果保存为新的CSV文件
    filtered_df.to_csv(out_filepath, index=False)


def filter_quality_1(filepath, out_filepath, origin_type):
    # 读取CSV文件
    df = pd.read_csv(filepath)
    # 筛选至少有三列专家判定为 'wet' 的行
    # axis=1 表示按行进行判断
    filtered_df = df[(df[['severity_1', 'severity_2', 'severity_3', 'severity_4']] == origin_type).sum(axis=1) >= 1]

    # 将筛选结果保存为新的CSV文件
    filtered_df.to_csv(out_filepath, index=False)


filepath = "four_non_nan.csv"
out_filepath = "four_non_nan_pseudocough.csv"
filter_quality(filepath, out_filepath, origin_type="pseudocough")

out_filepath = "four_non_nan_mild.csv"
filter_quality(filepath, out_filepath, origin_type="mild")

out_filepath = "four_non_nan_severe.csv"
filter_quality(filepath, out_filepath, origin_type="severe")

filepath = "one_non_nan_good.csv"
out_filepath = "one_non_nan_pseudocough.csv"
filter_quality_1(filepath, out_filepath, origin_type="pseudocough")

out_filepath = "one_non_nan_mild.csv"
filter_quality_1(filepath, out_filepath, origin_type="mild")

out_filepath = "one_non_nan_severe.csv"
filter_quality_1(filepath, out_filepath, origin_type="severe")

out_filepath = "one_non_nan_healthy_cough.csv"
filter_quality_1(filepath, out_filepath, origin_type="healthy_cough")
if __name__ == '__main__':
    pass
