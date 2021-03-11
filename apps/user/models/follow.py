from django.db import models

from .user import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', help_text='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', help_text='following', on_delete=models.CASCADE)
