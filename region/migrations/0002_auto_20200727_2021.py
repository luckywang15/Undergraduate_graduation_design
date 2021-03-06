# Generated by Django 3.0.8 on 2020-07-27 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': '区域信息', 'verbose_name_plural': '区域信息'},
        ),
        migrations.AddField(
            model_name='region',
            name='is_display',
            field=models.BooleanField(default=False, verbose_name='是否在地图上展示'),
        ),
        migrations.AddField(
            model_name='region',
            name='is_municipality',
            field=models.BooleanField(default=False, null=True, verbose_name='是否为直辖市'),
        ),
        migrations.AddField(
            model_name='region',
            name='is_province_capital',
            field=models.BooleanField(default=False, null=True, verbose_name='是否为省会'),
        ),
        migrations.AddField(
            model_name='region',
            name='is_province_municipality',
            field=models.BooleanField(default=False, null=True, verbose_name='是否为省直辖'),
        ),
        migrations.AddField(
            model_name='region',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='纬度'),
        ),
        migrations.AddField(
            model_name='region',
            name='level',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='区域级别'),
        ),
        migrations.AddField(
            model_name='region',
            name='longtitude',
            field=models.FloatField(blank=True, null=True, verbose_name='经度'),
        ),
    ]
