from django.contrib import admin

from .models.fiveapp import *


# admin.site.register(Person)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'password']
    list_display_links = ['email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['publisher', 'title', 'content','slug', 'publish_date']
    list_display_links = ['title']
    readonly_fields = ['slug', 'publish_date']