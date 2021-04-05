from django import template

register = template.Library()


# post
@register.simple_tag
def like_count(likes):
    """
    returns count of members liked this post
    """
    return int(bool(likes.all())) * likes.count()
