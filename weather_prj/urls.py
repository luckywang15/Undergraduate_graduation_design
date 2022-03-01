"""weather_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from comments.views import show_comments
from weather_data.views import region_weather, max_degree, min_degree, wind_power, recommend, dif_in_tempt, roadline
from weather_prj import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用于获取地区天气
    path('region/<int:region_id>', region_weather),
    path('roadline/', roadline),
    path('max_degree/', max_degree),
    path('min_degree/', min_degree),
    path('wind_power/', wind_power),
    path('dif_in_tempt/', dif_in_tempt),
    path('comments/', show_comments),  #设置留言板路由
    path('', recommend),
]

# 配置静态文件的路由（从配置文件里读取配置项再进行操作）：
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
