# -*- coding:utf8 -*-
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings
from PIL import Image
import os


def make_thumb(path, size=600):
    """
    上传图片生成缩略
    """
    image_buf = Image.open(path)
    width, height = image_buf.size
    if width > size:
        delta = width / size
        height = int(height / delta)
        image_buf.thumbnail((size, height), Image.ANTIALIAS)
        return image_buf


def del_image(path):
    """
    删除配图
    """
    if os.path.isfile(path):
        os.remove(path)


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
    abstract = models.CharField(verbose_name=u'文章摘要', max_length=256, blank=True)
    text = models.TextField(verbose_name=u"正文")
    status = models.CharField(verbose_name=u'状态', max_length=1, choices=_STATUS_CHOICES, default='p')
    created = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)

    def __str__(self):
        return self.title

    def delete(self):
        """
        删除文章的同时删除文件系统中相关图片
        """
        images_of_article = self.images.all()

        if images_of_article:
            for image_of_article in images_of_article:
                del_image(os.path.join(settings.MEDIA_ROOT, image_of_article.image.name))
                if image_of_article.thumb:
                    del_image(os.path.join(settings.MEDIA_ROOT, image_of_article.thumb.name))
            super().delete()
        else:
            super().delete()

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'


class ArticleImages(models.Model):
    """
    配图
    """
    article = models.ForeignKey(Article, verbose_name=u'文章', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', verbose_name=u"配图", blank=True)
    thumb = models.ImageField(upload_to='uploads/thumb_images', verbose_name=u"缩略图", blank=True)
    upload_time = models.DateTimeField(verbose_name=u"图片上传时间", auto_now_add=True)

    def __str__(self):
        return u'%s %s' % (self.image.name, self.article.title)

    def save(self, *args, **kwargs):
        """
        存储数据同时生成图片缩略图
        """
        super().save()
        base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_buf = make_thumb(self.image.path)
        if thumb_buf:
            relate_thumb_path = os.path.join('uploads/thumb_images', base + '.thumb' + ext)
            thumb_path = os.path.join(settings.MEDIA_ROOT, relate_thumb_path)
            thumb_buf.save(thumb_path)
            self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
            super().save()

    class Meta:
        db_table = "upload_images"
        verbose_name_plural = verbose_name = u"配图"
