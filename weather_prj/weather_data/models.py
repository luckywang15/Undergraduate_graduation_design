from django.db import models
from region.models import Region


# Create your models here.
class WeatherData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    day_weather = models.CharField(max_length=20, blank=True, null=True)
    day_weather_code = models.CharField(max_length=4)
    day_weather_short = models.CharField(max_length=20, blank=True, null=True)
    day_wind_direction = models.CharField(max_length=20, blank=True, null=True)
    day_wind_direction_code = models.CharField(max_length=4)
    day_wind_power = models.SmallIntegerField(blank=True,null=True)
    day_wind_power_code = models.CharField(max_length=4)
    max_degree = models.FloatField()
    min_degree = models.FloatField()
    night_weather = models.CharField(max_length=20, blank=True, null=True)
    night_weather_code = models.CharField(max_length=4)
    night_weather_short = models.CharField(max_length=20, blank=True, null=True)
    night_wind_direction = models.CharField(max_length=20, blank=True, null=True)
    night_wind_direction_code = models.CharField(max_length=4)
    night_wind_power = models.CharField(max_length=20, blank=True, null=True)
    night_wind_power_code = models.CharField(max_length=4)
    time = models.DateField()
    # 用于记录天气数据是什么时候插入数据库的
    # auto_now_add = True 自动将当前时间添加到字段中
    created = models.DateTimeField(auto_now_add=True)


class WeatherResult(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    result = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']  # 按照created降序排序
