from django.db import models

from messenger import settings


class Follow(models.Model):
    """
    to save follow records. follower can see following posts on their timeline.
    if Member A follows member B, it doesn't mean B follows A, too.
    member A needs to send a request to follow member B and that's when a Follow object is created. if member B rejects
    the request, or member A takes back the request, or member A unfollow member B after their follow request was
    accepted, record will be deleted from database.
    """
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', verbose_name='follower'
                                 , on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', verbose_name='following'
                                  , on_delete=models.CASCADE)
    request_accepted = models.BooleanField('Request Accepted', default=False)  # if true, it means following has
    # accepted follower's request. if false, it means follower has requested but following hasn't decided to accept or
    # decline the request yet.
