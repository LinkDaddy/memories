from pagedown.widgets import AdminPagedownWidget
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """
    用于 Pagedown 扩展 admin 增加文章表单
    """
    text = forms.CharField(label='正文', widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'
