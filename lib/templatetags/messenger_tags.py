from django import template

from common.utilities import seconds_to_time_unit

register = template.Library()


@register.filter
def typed(obj):
    return type(obj)


@register.filter
def custom_time_format(date_time):
    return seconds_to_time_unit(date_time)


@register.filter
def email_format(email):
    return email.split('@')[0]
