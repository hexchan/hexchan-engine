from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from ..models import ContentBlock


@admin.register(ContentBlock)
class ContentBlockAdmin(MarkdownxModelAdmin):
    list_display = ('hid', 'is_active')
