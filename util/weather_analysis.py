#  该模块用于天气数据分析的相关脚本

from pandas import DataFrame
import pandas as pd
import util
from region.models import Region
from util.normalization import wind_power_normalization, weather_type_normalization, sigmoid
from weather_data.models import WeatherData, WeatherResult

# 获取区域未来六天的天气数据 以列表+字典的形式返回数据
from weather_prj.settings import OPTIMUM_MAX_TEMP, OPTIMUM_MIN_TEMP, WEIGHTS_DICT


def get_region_weather_data(region: Region):
    return WeatherData.objects.filter(region=region).order_by('-created')[:6].values('day_weather', 'day_weather_code',
                                                                                     'day_wind_power', 'max_degree',
                                                                                     'min_degree')


# 获取区域天气数据对应的日期， 以列表形式返回数据
def get_region_weather_date(region: Region) -> list:
    return WeatherData.objects.filter(region=region).order_by('-created')[:6].values_list('time')


# 将区域的天气数据整理成DataFrame的形式
def get_region_weather_dataframe(region: Region) -> DataFrame:
    data = get_region_weather_data(region)
    date = get_region_weather_date(region)
    return pd.DataFrame(data, index=date)


def normalize_region_weather(region):
    df = get_region_weather_dataframe(region)
    new_df = pd.DataFrame()
    new_df['max_degree'] = 1.4 - (df['max_degree'] - OPTIMUM_MAX_TEMP).abs().apply(sigmoid)
    new_df['min_degree'] = 1.4 - (df['min_degree'] - OPTIMUM_MIN_TEMP).abs().apply(sigmoid)
    new_df['dif_in_tempt'] = 1.3 - (df['max_degree'] - df['min_degree']).apply(sigmoid)
    new_df['day_wind_power'] = df['day_wind_power'].apply(wind_power_normalization)
    new_df['day_weather_code'] = df['day_weather_code'].apply(weather_type_normalization)
    return new_df


def calculate_region_result(region):
    try:
        df = normalize_region_weather(region)
        weights = pd.Series(WEIGHTS_DICT)
        return (df @ weights).sum()
    except:
        return 0


def save_display_region_result():
    region_list = Region.objects.filter(is_display=True)
    for r in region_list:
        WeatherResult.objects.create(region=r, result=calculate_region_result(r))
        print(f"{r.name}结果保存成功")

def delete_weatherresult_all():
    """
    删除所有天气旅游指数数据
    :return:
    """
    data = WeatherResult.objects.all()
    if data.count() > 0:
        print(data.delete())

if __name__ == '__main__':
    # region = Region.objects.get(name='荆州市')
    # print(get_region_weather_data(region))
    # print(get_region_weather_date(region))
    # df = pd.DataFrame(get_region_weather_data(region))
    # df = get_region_weather_dataframe(region)
    # print(df)
    # print(normalize_region_weather(region))
    # print(calculate_region_result(region))
    delete_weatherresult_all()
    save_display_region_result()
    # calculate_region_result(region)
