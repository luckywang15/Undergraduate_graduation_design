import os
import django
#  手动启动django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_prj.settings')
# 启动django
django.setup()
