# -*- coding:utf8 -*-
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os


def _add_thumb(s):
    """
    往图片文件名里添加'.thumb'
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path)

    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return _add_thumb(self.url)

    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super().save(name, content, save)
        img = Image.open(self.path)

        width, height = img.size

        thumb_width = 0
        thumb_height = 0

        # 根据图片长宽比判断图片布局（横、竖）执行不同的等比压缩策略
        if width / height >= 1:
            if width > self.field.limit_width:
                delta = width / self.field.limit_width
                thumb_width = self.field.limit_width
                thumb_height = int(height / delta)
        else:
            if height > self.field.limit_height:
                delta = height / self.field.limit_height
                thumb_width = int(width / delta)
                thumb_height = self.field.limit_height

        if thumb_width != 0 and thumb_height != 0:
            img.thumbnail(
                (thumb_width, thumb_height),
                Image.ANTIALIAS
            )
            img.save(self.thumb_path)

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)

        super().delete(save)


class ThumbnailImageField(ImageField):
    """
    生成JPEG格式的缩略图，
    接受两个可选参数，缩略图的宽和高，默认设置为128px；
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, limit_width=128, limit_height=128, *args, **kwargs):
        self.limit_width = limit_width
        self.limit_height = limit_height
        super().__init__(*args, **kwargs)
