# -*- coding:utf8 -*-
from django.db import models
from .fields import ThumbnailImageField
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(verbose_name=u"标签名称", max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class Article(models.Model):
    """
    文章
    """
    _STATUS_CHOICES = (
        ('d', u'草稿'),
        ('p', u'发布'),
    )
    title = models.CharField(verbose_name=u"文章标题", max_length=256)
    tag = models.ManyToManyField(Tag, verbose_name=u'标签', blank=True)
    text = models.TextField(verbose_name=u"正文")
    status = models.CharField(verbose_name=u'状态', max_length=1, choices=_STATUS_CHOICES, default='p')
    created = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'


class Album(models.Model):
    """
    相册，用于文章配图分组。
    """
    name = models.CharField(verbose_name=u'相册名称', max_length=256)
    remark = models.CharField(verbose_name=u'相册备注', max_length=512)
    created = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'相册'
        verbose_name_plural = u'相册'


class ArticleImages(models.Model):
    """
    配图
    """
    album = models.ForeignKey(Album, verbose_name=u'相册', related_name='photos', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name=u'文章', related_name='images', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=u'标题', max_length=128, blank=True)
    photo = ThumbnailImageField(verbose_name=u"照片", upload_to='uploads/photo/%Y/%m/%d', limit_height=600,
                                limit_width=600)
    upload_time = models.DateTimeField(verbose_name=u"图片上传时间", auto_now_add=True)
    like = models.IntegerField(verbose_name=u'点赞数', default=0)

    def __str__(self):
        return self.title

    @property
    def thum_photo(self):
        return self.photo.thumb_url

    class Meta:
        verbose_name_plural = verbose_name = u"配图"


@receiver(post_delete, sender=ArticleImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(pre_save, sender=ArticleImages)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).photo
    except sender.DoesNotExist:
        return False

    new_file = instance.photo
    if not old_file == new_file:
        old_file.delete(save=False)
