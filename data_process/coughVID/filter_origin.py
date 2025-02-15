import pandas as pd


def filter_quality(filepath,out_filepath,origin_type):
    # 读取CSV文件
    df = pd.read_csv(filepath)
    # 筛选至少有三列专家判定为 'wet' 的行
    # axis=1 表示按行进行判断
    filtered_df = df[(df[['diagnosis_1', 'diagnosis_2', 'diagnosis_3', 'diagnosis_4']] == origin_type).sum(axis=1) >= 3]

    # 将筛选结果保存为新的CSV文件
    filtered_df.to_csv(out_filepath, index=False)


# filepath = "filtered_dry_output.csv"
# out_filepath = "filtered_dry_output_good.csv"

filepath = "four_non_nan.csv"
out_filepath = "four_non_nan_lower_infection.csv"
filter_quality(filepath, out_filepath,origin_type="lower_infection")

filepath = "four_non_nan.csv"
out_filepath = "four_non_nan_upper_infection.csv"
filter_quality(filepath, out_filepath,origin_type="upper_infection")

filepath = "four_non_nan.csv"
out_filepath = "four_non_nan_COVID-19.csv"
filter_quality(filepath, out_filepath,origin_type="COVID-19")

filepath = "four_non_nan.csv"
out_filepath = "four_non_nan_healthy_cough.csv"
filter_quality(filepath, out_filepath,origin_type="healthy_cough")



def filter_quality_1(filepath,out_filepath,origin_type):
    # 读取CSV文件
    df = pd.read_csv(filepath)
    # 筛选至少有三列专家判定为 'wet' 的行
    # axis=1 表示按行进行判断
    filtered_df = df[(df[['diagnosis_1', 'diagnosis_2', 'diagnosis_3', 'diagnosis_4']] == origin_type).sum(axis=1) >= 1]

    # 将筛选结果保存为新的CSV文件
    filtered_df.to_csv(out_filepath, index=False)


# filepath = "filtered_dry_output.csv"
# out_filepath = "filtered_dry_output_good.csv"

filepath = "one_non_nan_good.csv"
out_filepath = "one_non_nan_lower_infection.csv"
filter_quality_1(filepath, out_filepath,origin_type="lower_infection")

out_filepath = "one_non_nan_upper_infection.csv"
filter_quality_1(filepath, out_filepath,origin_type="upper_infection")

out_filepath = "one_non_nan_COVID-19.csv"
filter_quality_1(filepath, out_filepath,origin_type="COVID-19")

out_filepath = "one_non_nan_healthy_cough.csv"
filter_quality_1(filepath, out_filepath,origin_type="healthy_cough")
if __name__ == '__main__':
    pass
