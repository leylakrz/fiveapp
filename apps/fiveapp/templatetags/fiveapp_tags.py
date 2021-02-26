from django import template
from django.template.defaultfilters import timesince_filter
from django.utils.timezone import now

from common.utilities import seconds_to_time_unit

register = template.Library()


@register.inclusion_tag('nav.html')
def custom_nav(user_id):
    return {'user_id': user_id}


@register.filter
def typed(obj):
    return type(obj)


@register.filter
def custom_time_format(date_time):
    seconds = int((now() - date_time).total_seconds())
    if seconds > 0:
        return seconds_to_time_unit(seconds)


@register.filter
def email_format(email):
    return email.split('@')[0]
