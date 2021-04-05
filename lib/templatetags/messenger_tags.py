from django import template

from apps.event.models import *
from apps.post.models import Post, Comment
from common.utilities import seconds_to_time_unit

register = template.Library()


@register.filter
def typed(obj):
    """
    gets a post's title capitalizes the first character.
    """
    return type(obj)


@register.filter
def custom_time_format(date_time):
    """
    return passed time since post/comment publication or member's registration in the longest time format like day,
    week, etc.
    """
    return seconds_to_time_unit(date_time)


@register.inclusion_tag('lib/latest_events.html')
def latest_events(user):
    """
    returns 5 latest notifications (events).
    """
    events = Event.objects.filter(viewer=user).order_by('-date')[:5]
    return {'events': events}


@register.simple_tag
def get_title_by_post(post_id):
    """
    returns title of the liked post to show on side bar, in related notification (event).
    """
    return Post.objects.get(pk=post_id).title


@register.simple_tag
def get_title_by_comment(comment_id):
    """
    returns title of the commented post to show on side bar, in related notification (event).
    """
    return Comment.objects.get(pk=comment_id).post.title


@register.filter
def get_slug_by_post(post_id):
    """
    returns slug of the liked post to show on side bar, in related notification (event). used in <a> tag.
    """
    return Post.objects.get(pk=post_id).slug


@register.filter
def get_slug_by_comment(comment_id):
    """
    returns slug of the commented post to show on side bar, in related notification (event). used in <a> tag.
    """
    return Comment.objects.get(pk=comment_id).post.slug
