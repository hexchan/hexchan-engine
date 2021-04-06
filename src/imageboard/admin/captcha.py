from django.contrib import admin
from django.utils.html import format_html

from imageboard.models.captcha import Captcha


@admin.register(Captcha)
class CaptchaAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'solution', 'thumbnail')
    readonly_fields = ('id', 'thumbnail',)
    fields = ('id', 'public_id', 'solution', 'thumbnail', 'image',)

    def thumbnail(self, obj):
        return format_html(
            '<img src={} alt={} style="width: 200px; height: 40px;" />',
            obj.image,
            obj.solution,
        )
    thumbnail.short_description = 'Thumbnail'
