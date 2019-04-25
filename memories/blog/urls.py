from django.urls import path
from .views import ArticlesView, ArticleView, DateArchiveView, About

urlpatterns = [
    path('', ArticlesView.as_view(), name='list'),
    path('about/', About.as_view(), name='about'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='detail'),
    path('archive/timeline/', DateArchiveView.as_view(), name='timeline'),
]
