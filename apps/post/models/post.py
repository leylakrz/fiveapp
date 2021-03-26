import os

from django.db import models

# Create your models here.
from django.urls import reverse, NoReverseMatch
from django.utils.timezone import now
from django_extensions.db.fields import AutoSlugField

from messenger import settings


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Publisher', related_name='publisher',
                                  on_delete=models.DO_NOTHING)
    content = models.TextField('Content', null=True, blank=True)
    photo = models.ImageField(verbose_name='Photo', upload_to='post', null=True, blank=True)
    publish_date = models.DateTimeField('Publish Date', auto_now_add=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='liked by')
    slug = AutoSlugField('slug', populate_from=['title'], unique=True, default='')

    @property
    def age(self):
        return int((now() - self.publish_date).total_seconds())

    def __str__(self):
        return self.slug + str(self.publish_date)

    def get_absolute_url(self):
        try:
            return reverse('post', args=[self.slug])
        except NoReverseMatch:
            pass

    def save(self, *args, **kwargs):
        """
        if the photo is changed, deletes the previous one.
        """
        if self.id:
            old_photo = Post.objects.get(pk=self.id).photo
            if old_photo and (self.photo != old_photo):
                os.remove(old_photo.path)
        super(Post, self).save(*args, **kwargs)
