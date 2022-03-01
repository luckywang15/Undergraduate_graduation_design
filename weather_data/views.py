# Create your views here.
from django.contrib import messages
import time
from region.models import Region
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta

from util.spider_weather import delete_weather_by_region, get_weather_by_region, delete_weather_dbfyesterday, get_weather_by_display_regions
from util.weather_analysis import calculate_region_result, delete_weatherresult_all, save_display_region_result
from weather_data.form import RegionForm
from weather_data.models import WeatherData, WeatherResult
from django.shortcuts import render

from weather_prj.settings import WEATHER_DATE_START, WEATHER_DATE_END

# 设置定时任务，随Django执行而执行
# 使用下面这行可以使你的定时任务在后台运行
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 日常执行数据爬取
def dailytask():
    delete_weather_dbfyesterday()
    get_weather_by_display_regions()
    delete_weatherresult_all()
    save_display_region_result()

scheduler = BackgroundScheduler()
# 每周一到周天早上0点运行dailytask
scheduler.add_job(func=dailytask, trigger='cron', day_of_week='0-6', hour=13, minute=45)
scheduler.start()
# 每次随Django启动就执行一次
# try:
#     dailytask()
# except:
#     pass

def region_weather(request, region_id):
    region = Region.objects.get(id=region_id)
    region_list = Region.objects.filter(level='0')

    if request.method == 'POST':
        # print(request.POST)
        # 使用表单对象，处理用户发来的信息
        form = RegionForm(request.POST)
        # 对表单的数据做校验的is_valid()，返回True或False
        # is_valid()方法，会把校验成功的数据转换成可用的数据类型，放在cleaned_data属性中
        # print(form.is_valid())
        # print(form.cleaned_data)
        # 修改相应数据库内容
        if form.is_valid():
            region.short_name = form.cleaned_data.get('short_name')
            region.latitude = form.cleaned_data.get('latitude')
            region.longtitude = form.cleaned_data.get('longtitude')
            region.is_display = form.cleaned_data.get('is_display')
            region.save()
            # Django提供了基于Cookie或者会话的消息框架messages，无论是匿名用户还是认证的用户。
            # 这个消息框架允许你临时将消息存储在请求中，并在接下来的请求（通常就是下一个请求）中提取它们并显示。
            # 每个消息都带有一个特定的level标签，表示其优先级（例如info、 warning或error）。
            messages.success(request, '城市信息修改成功！', extra_tags='success')
        else:
            messages.error(request, '输入数据有误，修改失败！', extra_tags='danger')
        #  重定向响应ResponseRedirect，以get请求方式跳回原页面，避免刷新时出现表单提交验证提醒
        return HttpResponseRedirect(request.path)
    data = WeatherData.objects.filter(region_id=region_id, time__range=(WEATHER_DATE_START, WEATHER_DATE_END))

    if data.count() < 8:
        # 清除该地区在数据库中的老数据
        delete_weather_by_region(region)
        new_data = get_weather_by_region(region)
        # 将实时查到的天气数据存到数据库里面
        for v in new_data.values():
            WeatherData.objects.create(region=region, **v)
        data = WeatherData.objects.filter(region_id=region_id, time__range=(WEATHER_DATE_START, WEATHER_DATE_END))
    # 查询该地区是否计算出天气推荐指数
    if not region.weatherresult_set.filter(created__day=datetime.now().day):
        WeatherResult.objects.create(region=region, result=calculate_region_result(region))

    # 详情页折线图
    date = []
    for d in data:
        date.append('%s'%(d.time))
    max_1 = []
    for y in data:
        max_1.append('%s' % (y.max_degree))
    min_1 = []
    for y in data:
        min_1.append('%s' % (y.min_degree))


    context = {
        'region': region,
        'data': data,
        'date': date,
        'max_1': max_1,
        'min_1': min_1,
        'region_list': region_list # 一级地区菜单
    }
    # render快捷函数，第一个参数为request，第二个为模板文件，第三个为上下文
    return render(request, 'weather_table.html', context)
    # template = loader.get_template('weather_table.html')
    # return HttpResponse(template.render(context))


# 城市最高温
def max_degree(request):
    # 让在地图上面展示的城市的温度显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                   .first().max_degree
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日最高温情况',
        'num': 1.5,
        'color': 'orangered',
        'land_color': '#004981',
        'boundary_color': '#029fd4',
        'name': '高温℃'
    }
    return render(request, 'map.html', context)


# 城市最低温
def min_degree(request):
    # 让在地图上面展示的城市的温度显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                   .first().min_degree
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日低温情况',
        'num': 1.2,
        'color': '#8ABBD1',
        'land_color': '#004981',
        'boundary_color': '#029fd4',
        'name': '最低温℃'
    }
    return render(request, 'map.html', context)


# 城市风力
def wind_power(request):
    # 让在地图上面展示的城市的风力等级显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                   .first().day_wind_power
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日风力等级情况',
        'num': 0.20,
        'color': '#FFC1C1',
        'land_color': '#004981',
        'boundary_color': '#029fd4',
        'name': '风力等级'
    }
    return render(request, 'map.html', context)


# 城市温差
def dif_in_tempt(request):
    # 让在地图上面展示的城市的温差显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                            .first().max_degree - r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                            .first().min_degree
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日昼夜温差情况',
        'num': 0.5,
        'color': '#CD5C5C',
        'land_color': '#004981',
        'boundary_color': '#029fd4',
        'name': '昼夜温差'
    }
    return render(request, 'map.html', context)


# 景点推荐指数
def recommend(request):
    # 让在地图上面展示的城市的温度显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherresult_set.first().result
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市旅游推荐指数',
        'subtitle': '根据未来6天天气情况计算出的是否适合旅游的情况',
        'num': 3.3,
        'color': '#ed8112',
        'land_color': '#323c48',
        'boundary_color': '#FFF8DC',
        'name': '推荐指数'
    }
    return render(request, 'map.html', context)

# 气温折线图
def degree(request):
    # 让在地图上面展示的城市的温度显示出来
    region_list = Region.objects.filter(is_display=True)
    data = []

def roadline(request):
    return render(request, 'roadline.html')
