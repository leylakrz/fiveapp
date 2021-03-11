from django import template
from django.utils.timezone import now

from common.utilities import seconds_to_time_unit

register = template.Library()


# post
@register.simple_tag
def like_count(likes):
    return int(bool(likes.all())) * likes.count()
