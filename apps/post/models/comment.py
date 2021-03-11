from django.db import models
from django.utils.timezone import now

from apps.user.models import User
from apps.post.models import Post


class Comment(models.Model):
    publisher = models.ForeignKey(User, help_text='Publisher', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, help_text='Post', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content')
    publish_date = models.DateTimeField('Publish Date')

    @property
    def age(self):
        return int((now() - self.publish_date).total_seconds())

    def __str__(self):
        return self.title + ': by ' + self.publisher.email + ' post: ' + self.post.title

    def save(self, *args, **kwargs):
        self.publish_date = now()
        super().save(*args, **kwargs)
