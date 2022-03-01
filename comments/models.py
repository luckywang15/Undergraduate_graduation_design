from django.db import models

# Create your models here.
class Comments_Board(models.Model):
    """评论留言板"""
    name = models.CharField(max_length=10)  # 留言人昵称长度限制10个字符
    content = models.TextField()  # 大文本字段
    time = models.DateTimeField(auto_now_add=True)  # 留言时间
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
