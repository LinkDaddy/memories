# -*- coding:utf8 -*-
from django.contrib import admin
from .models import Article, Tag, ArticleImages
from .forms import ArticleForm


class ArticleImagesAdmin(admin.StackedInline):
    model = ArticleImages
    admin.site.register(ArticleImages)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    filter_horizontal = ('tag',)

    form = ArticleForm

    inlines = [ArticleImagesAdmin, ]

    actions = ['del_article_and_img']

    def del_article_and_img(self, request, queryset):
        for article in queryset:
            article.delete()
    del_article_and_img.short_description = u'删除文章并删除文件系统上相关图片文件'


admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)

