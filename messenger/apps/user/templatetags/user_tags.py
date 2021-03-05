from django import template
from django.utils.timezone import now

from common.utilities import seconds_to_time_unit

from apps.user.models import Follow

register = template.Library()


@register.filter
def follower_count(user_id):
    count = Follow.objects.filter(following=user_id).count()
    return str(count) + ' Follower' + int(count > 1) * 's'


@register.filter
def following_count(user_id):
    count = Follow.objects.filter(follower=user_id).count()
    return str(count) + ' Following' + int(count > 1) * 's'
