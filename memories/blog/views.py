# -*- coding:utf8 -*-
from django.views.generic import ListView, DetailView
from blog.models import Article
from collections import OrderedDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class GlobalContextMixin(object):
    """
    设置站点信息
    """
    def get_context_data(self, **kwargs):
        """
        添加站点信息
        """
        context = super().get_context_data(**kwargs)
        article_count = Article.objects.count()

        context.setdefault('article_count', article_count)

        return context


class ArticlesView(GlobalContextMixin, ListView):
    """
    文章列表
    """
    queryset = Article.objects.filter(status='1').exclude(title="About")
    model = Article
    ordering = ('-created',)
    context_object_name = 'articles'

    template_name = 'index.html'
    paginate_by = 5


class ArticleView(GlobalContextMixin, DetailView):
    """
    文章详情
    """
    model = Article
    context_object_name = "article"
    template_name = "article.html"

    def get_object(self, queryset=None):
        obj = super().get_object()

        if obj.status != '1':
            raise Http404("抱歉没有对应的内容。")
        return obj


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
            articles = Article.objects.filter(status='o', created__year=date.year).exclude(title="About")
            archive_dict.setdefault(date, articles)

        context.setdefault('archive_dict', archive_dict)
        return context


class About(DetailView):
    """
    关于我
    """
    template_name = 'article.html'

    def get_object(self, queryset=Article.objects.all()):
        try:
            obj = queryset.get(title="About")
        except ObjectDoesNotExist:
            raise Http404("博主很懒，什么也没有写。")

        return obj
