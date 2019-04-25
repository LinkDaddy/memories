from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from sorl.thumbnail import ImageField
from sorl.thumbnail import delete
import datetime
import uuid
import os


def generate_filename(instance, filename):
    """
    生成图片文件名。
    """
    path = datetime.datetime.now().strftime('uploads/photo/%Y/%m/%d')

    photo_name = uuid.uuid5(uuid.NAMESPACE_DNS, filename).hex + os.path.splitext(filename)[-1]

    return os.path.join(path, photo_name)


class Photo(models.Model):
    """
    图片
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    photo = ImageField(verbose_name="照片", upload_to=generate_filename)
    upload_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    like = models.IntegerField(verbose_name="赞", default=0)
    comment = models.TextField(verbose_name="说明", blank=True)

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "图片"

    def __str__(self):
        return self.photo.path


generic_relation = GenericRelation(Photo, related_query_name='photos')


@receiver(post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.photo:
        delete(instance.photo.path)


@receiver(pre_save, sender=Photo)
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
        delete(old_file.path)
