from django.contrib import admin

# Register your models here.
from apps.member.models import Member, Follow


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'register_time']
    list_display_links = ['email', 'first_name', 'last_name']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
    list_display_links = ['follower', 'following']
