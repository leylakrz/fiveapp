from django.contrib import admin

# Register your models here.
from apps.post.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['publisher', 'title', 'content', 'slug', 'publish_date']
    list_display_links = ['title', 'slug', 'publish_date']
    readonly_fields = ['slug', 'publish_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['publisher', 'post', 'title', 'publish_date']
    list_display_links = ['title', 'publish_date']
    readonly_fields = ['publish_date']
