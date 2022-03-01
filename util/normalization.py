import numpy as np


# sigmoid归一化处理函数
def sigmoid(X):
    return 1.0 / (1 + np.exp(-float(X)))


# # 对温度的归一化处理
# def normalize_region_weather(region):
#     df = get_region_weather_dataframe(region)
#     new_df = pd.DataFrame()
#     new_df['max_degree'] = 1.5 - (df['max_degree'] - OPTIMUM_MAX_TEMP).abs().apply(sigmoid)
#     new_df['min_degree'] = 1.5 - (df['min_degree'] - OPTIMUM_MIN_TEMP).abs().apply(sigmoid)
#     return new_df
#
#

# 对风力的归一化处理
def wind_power_normalization(level):
    if level < 2:
        return 0.6
    elif 2 <= level < 4:
        return 1
    elif 4 <= level < 6:
        return 0.3
    else:
        return 0


# 对天气情况进行归一化处理
def weather_type_normalization(code):
    if code in ['00', '01', '02']:
        return 1
    elif code in ['03', '04', '07', '08', '18', '21']:
        return 0.4
    elif code in ['09', '10', '22', '23', '24']:
        return 0
