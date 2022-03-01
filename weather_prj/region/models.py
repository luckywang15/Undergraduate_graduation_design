from django.db import models


# Create your models here.
class Region(models.Model):
    id = models.IntegerField('区域编号', primary_key=True)
    name = models.CharField('区域名称', max_length=30, null=False, blank=False)
    short_name = models.CharField('区域别名', max_length=30, null=False, blank=False)
    #  自关联外键字段   null=True表示在数据库中表中存储时允许为空
    #  related_name用于指定 1找多时，使用的名称 verbose_name:说明文字
    parent = models.ForeignKey('self', verbose_name='父级区域',
                               related_name='children',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    # 为每个区域 生一个字段  level 用于表名当前这个region是几级的？ 0,1,2,3
    level = models.CharField('区域级别', max_length=2, null=True, blank=True)
    latitude = models.FloatField('纬度', null=True, blank=True)
    longtitude = models.FloatField('经度', null=True, blank=True)
    # 标志位： 直辖市 标志出来
    is_municipality = models.BooleanField('是否为直辖市', default=False, null=True)
    # 标志位 是否为省会城市
    is_province_capital = models.BooleanField('是否为省会', default=False, null=True)
    # 标志位 是否为省直辖城市
    is_province_municipality = models.BooleanField('是否为省直辖', default=False, null=True)
    # 标志位 决定是否在地图上显示
    is_display = models.BooleanField('是否在地图上展示', default=False)

    def __str__(self):
        return self.name

    # 获取区域的省份名字
    def get_province_name(self):
        if self.level == '0':
            return self.name
        elif self.level == '1':
            return self.parent.name
        elif self.level == '2':
            return self.parent.parent.name
        else:
            return self.name

    class Meta:
        verbose_name = '区域信息'
        verbose_name_plural = verbose_name
