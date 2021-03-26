from django import template

from apps.member.models import Follow

register = template.Library()


@register.filter
def follower_count(user_id):
    count = Follow.objects.filter(following=user_id, request_accepted=True).count()
    return str(count) + ' Follower' + int(count > 1) * 's'


@register.filter
def following_count(user_id):
    count = Follow.objects.filter(follower=user_id, request_accepted=True).count()
    return str(count) + ' Following' + int(count > 1) * 's'


@register.filter
def if_none(value):
    if not value:
        return 'Unknown'
    return value
