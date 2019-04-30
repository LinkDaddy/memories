from django.contrib import admin
from .models import Article
from .forms import ArticleForm
from photoshow.admin import PhotoInlineAdmin


class ArticleAdmin(admin.ModelAdmin):
    fields = (('title', 'status', 'changed'), 'content')
    readonly_fields = ('changed',)
    list_display = ('title', 'created', 'changed', 'status')
    list_filter = ('created', 'changed')
    date_hierarchy = 'created'
    ordering = ('-created', 'changed')
    search_fields = ('title',)

    save_as = True

    form = ArticleForm

    inlines = [PhotoInlineAdmin]


admin.site.register(Article, ArticleAdmin)
