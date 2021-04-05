from django.contrib import admin

# Register your models here.
from apps.event.models import Event


@admin.register(Event)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['type', 'viewer', 'operator', 'date', 'foreign_key']
    list_display_links = ['date', 'foreign_key', 'type']
