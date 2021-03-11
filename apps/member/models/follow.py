from django.db import models

from messenger import settings


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', verbose_name='follower'
                                 , on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', verbose_name='following'
                                  , on_delete=models.CASCADE)
    request_accepted = models.BooleanField('Request Accepted', default=False)
