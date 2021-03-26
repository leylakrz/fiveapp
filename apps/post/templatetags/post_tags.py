from django import template

register = template.Library()


# post
@register.simple_tag
def like_count(likes):
    return int(bool(likes.all())) * likes.count()
