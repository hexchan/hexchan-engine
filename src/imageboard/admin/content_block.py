from django.contrib import admin

from ..models import ContentBlock


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('hid', 'is_active')
