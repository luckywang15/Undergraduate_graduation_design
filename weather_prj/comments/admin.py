from django.contrib import admin

# Register your models here.
from comments.models import Comments_Board

# 自定义后台界面
class Comments_BoardAdmin(admin.ModelAdmin):
    # 后台展示字段
    list_display = ['name', 'content', 'time']
    # 可直接在后台编辑
    list_editable = ['content']

admin.site.register(Comments_Board, Comments_BoardAdmin)