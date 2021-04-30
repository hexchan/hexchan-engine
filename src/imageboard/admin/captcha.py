from django.contrib import admin
from django.utils.html import format_html

from imageboard.models.captcha import Captcha
from imageboard.utils.captchamaker import bytes_to_base64, CAPTCHA_WIDTH, CAPTCHA_HEIGHT


@admin.register(Captcha)
class CaptchaAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'thread', 'ip_address', 'solution', 'thumbnail')
    readonly_fields = ('id', 'board', 'thread', 'ip_address', 'solution', 'thumbnail')
    fields = ('id', 'board', 'thread', 'ip_address', 'solution', 'thumbnail')

    def thumbnail(self, obj):
        return format_html(
            '<img src="{}" alt="{}" style="width: {}px; height: {}px;" />',
            bytes_to_base64(obj.image),
            obj.solution,
            CAPTCHA_WIDTH,
            CAPTCHA_HEIGHT
        )
    thumbnail.short_description = 'Thumbnail'
