from django.db import models
from photoshow.models import generic_relation


class Article(models.Model):
    """
    文章
    """
    _STATUS_CHOICES = (
        ('0', '草稿'),
        ('1', '公开'),
    )
    title = models.CharField(verbose_name="文章标题", max_length=256, unique=True)
    content = models.TextField(verbose_name="正文")
    status = models.CharField(verbose_name='状态', max_length=1, choices=_STATUS_CHOICES, default='0')
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    changed = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    photo = generic_relation

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'

    def __str__(self):
        return self.title
