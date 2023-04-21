from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def trout_version():
    return settings.TROUT_VERSION
