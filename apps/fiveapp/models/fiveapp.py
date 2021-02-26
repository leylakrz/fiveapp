import os
from random import randrange

from django.db import models, IntegrityError

# Create your models here.
from django.utils.text import slugify
from django.utils.timezone import now

from apps.fiveapp.manager import *


class User(models.Model):
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Password', max_length=50)
    register_time = models.DateTimeField('Registered At')
    salt = models.BinaryField('SALT')

    objects = UserManager()

    def __str__(self):
        return self.email + ' - Joined At: ' + self.register_time.strftime("%m/%d/%Y, %H:%M:%S")

    def save(self, *args, **kwargs):
        self.salt = os.urandom(32)
        self.password = hashlib.pbkdf2_hmac('sha256',
                                            self.password.encode(),
                                            binascii.hexlify(self.salt),
                                            100000)
        self.register_time = now()
        super().save(*args, **kwargs)

    def get_absolute_url(self, url_name):
        pass


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    publisher = models.ForeignKey(User, help_text='Publisher', default=1, on_delete=models.DO_NOTHING)
    content = models.TextField('Content')
    publish_date = models.DateTimeField('Publish Date', default=now)
    slug = models.SlugField('slug', max_length=100, unique=True, default='')

    def __str__(self):
        return self.slug + str(self.publish_date)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:  # if this title already exists:
            self.slug += str(randrange(0, 1000))
            super().save(*args, **kwargs)
