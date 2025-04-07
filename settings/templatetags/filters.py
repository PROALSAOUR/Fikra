# settings/templatetags/filters.py

import html
from django import template

register = template.Library()

@register.filter
def html_unescape(value):
    """يفك ترميز HTML مثل &nbsp; و &amp;"""
    return html.unescape(value)
