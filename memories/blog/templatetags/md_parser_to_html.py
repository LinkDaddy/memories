# -*- coding:utf8 -*-
import markdown2
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='md_to_html', is_safe=True)
@stringfilter
def to_html(value):
    return mark_safe(markdown2.markdown(value, extras=["fenced-code-blocks"]))
