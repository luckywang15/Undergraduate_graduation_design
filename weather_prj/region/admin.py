from django.contrib import admin

# Register your models here.
from region.models import Region

# 自定义后台界面
class RegionAdmin(admin.ModelAdmin):
    # 后台展示字段
    list_display = ['id', 'name', 'parent']
    # 可直接在后台编辑
    list_editable = ['name']

admin.site.register(Region, RegionAdmin)
