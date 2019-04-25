from django.contrib import admin
from .models import Photo
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.contenttypes.admin import GenericTabularInline


class PhotoInlineAdmin(AdminImageMixin, GenericTabularInline):
    model = Photo
    fields = (('like', 'upload_time',), 'photo')
    readonly_fields = ('like', 'upload_time', )


admin.site.register(Photo)
