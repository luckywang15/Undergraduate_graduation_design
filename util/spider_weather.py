import requests
import util
# 根据区域城市来获取1日天气数据
from region.models import Region
from weather_prj.settings import TX_WEATHER_URL, TX_WEATHER_PARAMS, TX_WEATHER_HEADERS
from datetime import datetime, timedelta
from weather_data.models import WeatherData
import time, random


def get_weather_by_region(region: Region):
    """
    根据区域获取天气信息
    :param region: 传一个区域model对象
    :return: 返回7日天气信息的字典
    """
    params = TX_WEATHER_PARAMS
    params["province"] = region.get_province_name()
    params["city"] = region.short_name  # 通过城市别名查天气情况
    res = requests.get(TX_WEATHER_URL, params=params, headers=TX_WEATHER_HEADERS)
    time.sleep(random.random())
    return res.json()["data"]["forecast_24h"]


def get_weather_by_display_regions():
    """
    爬取要在地图上展示的城市的7日最后一日天气数据
    :return:
    """
    # 获取要展示的城市的region的列表
    region_list = Region.objects.filter(is_display=True)

    # 对区域进行遍历，根据区域列表中的区域，调用爬取函数进行天气数据的爬取
    for r in region_list:
        # data = dict([get_weather_by_region(r).popitem()])
        data = get_weather_by_region(r)
        if data:
            #  把今日最新天气数据保存到数据库中
            for v in data.values():
                WeatherData.objects.create(region=r, **v)
                print(f"{r.name}天气已经成功保存")
    print('pause')


def delete_weather_by_region(region: Region):
    """
    根据区域信息，删掉从当前时间开始 前一天到后6天共八天的天气数据
    删掉昨日天气
    :param region:
    :return:
    """
    start = datetime.now() - timedelta(days=0)
    end = datetime.now() + timedelta(days=6)
    data = WeatherData.objects.filter(time__gte=start, time__lte=end, region=region)
    if data.count() > 0:
        print(data.delete())


def delete_weather_dbfyesterday():
    """
    删除所有前天天气数据
    :return:
    """
    # start = datetime.now() - timedelta(days=2)
    # end = datetime.now() - timedelta(days=2)
    # data = WeatherData.objects.filter(time__gte=start, time__lte=end)
    data = WeatherData.objects.all()
    # data = WeatherData.objects.filter(time=start)
    if data.count() > 0:
        print(data.delete())


if __name__ == '__main__':
    # xg = Region.objects.get(name="孝感市")
    # print(dict([get_weather_by_region(xg).popitem()]))
    # print(delete_weather_by_region(xg))
    delete_weather_dbfyesterday()
    get_weather_by_display_regions()
