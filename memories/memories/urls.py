# -*- coding:utf8 -*-
from django.contrib import admin
from django.urls import path
from blog.views import ArticlesView, ArticleView, DateArchiveView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('articles/', ArticlesView.as_view(), name='list'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='detail'),
    path('archive/timeline/', DateArchiveView.as_view(), name='timeline'),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
