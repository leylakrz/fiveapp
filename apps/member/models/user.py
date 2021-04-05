from random import randint

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
from django.core.validators import RegexValidator
from django.urls import reverse, NoReverseMatch
from django.db import models
from django.utils.timezone import now

from apps.member.managers import MemberManager


class Member(AbstractBaseUser, PermissionsMixin):
    """
    users' information.
    uses django.authentication by inheriting from AbstractBaseUser, which provides password filed,
    log in and log out functionality, etc.
    inherits from 'PermissionsMixin' to enable permission necessity for some site features.
    """
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    email = models.EmailField('email address', unique=True)  # username.
    register_time = models.DateTimeField('date joined', auto_now_add=True)
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField('Gender', max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    website = models.CharField('Website Link', max_length=50, blank=True, null=True)  # website link.
    bio = models.TextField('Biography', blank=True, null=True)

    phone_regex = RegexValidator(regex=r'09[0-3][0-9]-?[0-9]{3}-?[0-9]{4}',
                                 message="Phone number must be entered in the format: '09121234567'.\
                                  exactly 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, null=True, unique=True)
    # necessary for authentication.

    is_active = models.BooleanField('Active', default=False)  # false means either member has registered but hasn't
    # been authenticated yet, or a staff or superuser has deactivated the account via admin panel.
    is_superuser = models.BooleanField('Superuser', default=False)  # whether or not member has access to admin panel.
    is_staff = models.BooleanField('Staff', default=False)  # whether or not member has permission to all features and
    # permissions.

    sms_code = models.CharField('Sms Code', max_length=4)  # used for authentication in case member chooses
    # authentication by sms.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MemberManager()

    @property
    def age(self):
        """
        returns time passed since member's registration.
        """
        return int((now() - self.register_time).total_seconds())

    def get_full_name(self):
        """
        returns member's full name, first name + last name.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        """
        returns member's profile url, specially called in generic views.
        """
        try:
            return reverse('profile', args=[self.id])
        except NoReverseMatch:
            pass

    def save(self, *args, **kwargs):
        if not self.id:
            self.sms_code = randint(1000, 9999)
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return self.email + ' - Joined At: ' + self.register_time.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        app_label = "member"
