from django.db import models
from django.utils.timezone import now

from apps.member.models import Member
from apps.post.models import Post


class Comment(models.Model):
    publisher = models.ForeignKey(Member, verbose_name='Publisher', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
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
