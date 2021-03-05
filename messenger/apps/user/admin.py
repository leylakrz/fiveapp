from django.contrib import admin


# Register your models here.
from apps.user.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'password']
    list_display_links = ['email']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
    list_display_links = ['follower', 'following']
