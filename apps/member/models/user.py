from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
from django.urls import reverse, NoReverseMatch
from django.db import models
from django.utils.timezone import now

from apps.member.managers import MemberManager


class Member(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    email = models.EmailField('email address', unique=True)
    register_time = models.DateTimeField('date joined', auto_now_add=True)
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField('Gender', max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    website = models.CharField('Website Link', max_length=50, blank=True, null=True)
    bio = models.TextField('Biography', blank=True, null=True)

    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MemberManager()

    @property
    def age(self):
        return int((now() - self.register_time).total_seconds())

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        try:
            return reverse('profile', args=[self.id])
        except NoReverseMatch:
            pass

    def __str__(self):
        return self.email + ' - Joined At: ' + self.register_time.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        app_label = "member"
