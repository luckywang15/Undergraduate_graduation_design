from django import forms


# django 中的 Form类
class RegionForm(forms.Form):
    # 这里的字段名不要写错了，否则post返回的会解析不了，is_valid()会返回False
    short_name = forms.CharField()
    latitude = forms.FloatField()
    longtitude = forms.FloatField()
    is_display = forms.BooleanField(required=False)
