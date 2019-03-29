# -*- coding:utf8 -*-
from django.views.generic import ListView, DetailView
from blog.models import Tag, Article
from collections import OrderedDict


class GlobalContextMixin(object):
    """
    设置站点信息
    """
    def get_context_data(self, **kwargs):
        """
        添加站点信息
        """
        # context = super(GlobalContextMixin, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        article_count = Article.objects.count()
        tag_count = Tag.objects.count()

        context.setdefault('article_count', article_count)
        context.setdefault('tag_count', tag_count)

        return context


class ArticlesView(GlobalContextMixin, ListView):
    """
    文章列表
    """
    queryset = Article.objects.filter(status='p').exclude(title="About")
    model = Article
    ordering = ('-created',)
    context_object_name = 'articles'

    template_name = 'articles.html'
    paginate_by = 2


class ArticleView(GlobalContextMixin, DetailView):
    """
    文章详情
    """
    # queryset = Article.objects.all()
    model = Article
    context_object_name = "article"
    template_name = "article.html"


class DateArchiveView(GlobalContextMixin, ListView):
    """
    时间归档
    """
    queryset = Article.objects.datetimes('created', 'year', order='DESC')
    context_object_name = 'dates'
    template_name = 'archive.html'

    def get_context_data(self, **kwargs):
        context = super(DateArchiveView, self).get_context_data(**kwargs)
        dates = context.get(self.context_object_name)

        archive_dict = OrderedDict()
        for date in dates:
            articles = Article.objects.filter(status='p', created__year=date.year).exclude(title="About")
            archive_dict.setdefault(date, articles)

        context.setdefault('archive_dict', archive_dict)
        return context

