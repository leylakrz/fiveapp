from django.db import models

from messenger import settings


class Event(models.Model):
    """
    Event object is created when:
        a member (operator) likes one of another member's (viewer) post.
        a member (operator) comments on one of another member's (viewer) post.
        a member (operator) requests to follow another member (viewer).
        a member (operator) accept follow request of another member (viewer).

    'like' event object is delete when operator takes back (unlike) viewer's post.
    'comment' event object is delete when operator deletes their comment on viewer's post.
    'follow' and 'accept' event object is delete when operator takes back their follow request or unfollows the viewer.
    """
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='viewer', verbose_name='Viewer',
                               on_delete=models.CASCADE)  # member viewing this event / notification on their sidebar.
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operator', verbose_name='Operator',
                                 on_delete=models.CASCADE)  # member who created this object by having an interaction
    # with the viewer.
    date = models.DateTimeField('Date', auto_now=True)

    foreign_key = models.IntegerField('Post Or Comment\'s Id', null=True, blank=True)  # pk of the liked post or
    # published comment, if type of the event is 'like' or 'comment'.

    TYPE_CHOICES = (
    ('like', 'like'), ('comment', 'comment'), ('follow', 'new follow request'), ('accept', 'follow request accepted'))
    type = models.CharField('Type', choices=TYPE_CHOICES, max_length=7)
