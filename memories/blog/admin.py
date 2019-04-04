# -*- coding:utf8 -*-
from django.contrib import admin
from .models import Article, Tag, Album, ArticleImages
from .forms import ArticleForm

from django.utils.html import format_html_join
from django.utils.safestring import mark_safe


class ArticleImagesAdmin(admin.StackedInline):
    model = ArticleImages
    # admin.site.register(ArticleImages)
    fields = (('album', 'title', 'like', 'upload_time',), 'photo', 'view_thum_photo',)
    readonly_fields = ('like', 'upload_time', 'view_thum_photo',)

    def view_thum_photo(self, obj):
        return obj.thum_photo

    view_thum_photo.short_description = '缩略图'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    filter_horizontal = ('tag',)

    save_as = True

    form = ArticleForm

    inlines = [ArticleImagesAdmin]

    def del_article_and_img(self, request, queryset):
        for article in queryset:
            article.delete()
    del_article_and_img.short_description = u'删除文章并删除文件系统上相关图片文件'


admin.site.register(Tag)
admin.site.register(Album)
admin.site.register(Article, ArticleAdmin)


