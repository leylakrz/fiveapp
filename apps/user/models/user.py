import os

from django.db import models

# Create your models here.
from django.utils.timezone import now

from apps.user.manager import *


class User(models.Model):
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Password', max_length=50)
    register_time = models.DateTimeField('Registered At')
    salt = models.BinaryField('SALT')

    objects = UserManager()

    @property
    def age(self):
        return int((now() - self.register_time).total_seconds())

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
