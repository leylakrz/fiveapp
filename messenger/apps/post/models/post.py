from random import randrange

from django.db import models, IntegrityError

# Create your models here.
from django.utils.text import slugify
from django.utils.timezone import now

from apps.user.models import User


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    publisher = models.ForeignKey(User, help_text='Publisher', related_name='publisher',
                                  on_delete=models.DO_NOTHING)
    content = models.TextField('Content')
    publish_date = models.DateTimeField('Publish Date', auto_now_add=True)
    liked = models.ManyToManyField(User, help_text='liked by')
    slug = models.SlugField('slug', max_length=100, unique=True, default='')

    @property
    def age(self):
        return int((now() - self.publish_date).total_seconds())

    def __str__(self):
        return self.slug + str(self.publish_date)

    def save(self, *args, **kwargs):
        if self.id:
            super().save(*args, **kwargs)
        else:
            # self.publish_date = now()
            self.slug = slugify(self.title)
            try:
                super().save(*args, **kwargs)
            except IntegrityError:  # if this title already exists:
                self.slug += str(randrange(0, 1000))
                super().save(*args, **kwargs)
