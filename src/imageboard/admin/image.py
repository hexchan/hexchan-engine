from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings

from ..models import Image
from hexchan import config


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('post', 'post__thread', 'post__thread__board')

    # List options
    # ==================================================================================================================
    list_per_page = 100

    ordering = ('-created_at',)

    list_display = ('id', 'admin_board_hid', 'admin_thread_hid', 'admin_post_hid', 'hid',
                    'thumbnail', 'original_name', 'created_at', 'is_spoiler', 'is_deleted',
                    )

    list_editable = ('is_spoiler', 'is_deleted',)

    list_filter = ('is_deleted', 'created_at', 'post__thread__board',)

    list_display_links = ('id',)

    preserve_filters = True

    # Editor options
    # ==================================================================================================================
    readonly_fields = (
        'id',

        'admin_board_hid',
        'admin_thread_hid',
        'admin_post_hid',

        'post',
        'original_name',
        'mimetype',
        'created_at',
        'size',
        'width',
        'height',
        'checksum',
        'thumb_width',
        'thumb_height',

        'thumbnail',
        'url',
        'hid',
    )

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                ('id', 'admin_board_hid', 'admin_thread_hid', 'admin_post_hid', 'hid',),
                ('created_at',),
                ('url',),
                ('thumbnail',),
            ),
        }),

        ('Image', {
            'fields': (
                'original_name',
                'width',
                'height',
                'size',
                'mimetype',
            ),
        }),

        ('Thumbnail', {
            'fields': (
                'thumb_width',
                'thumb_height',
            ),
        }),

        ('Flags', {
            'fields': (
                (
                    'is_spoiler',
                    'is_deleted',
                ),
            ),
        }),
    )

    # Custom fields
    # ==================================================================================================================
    def admin_post_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_post_change', args=(obj.post.id,)),
            config.POST_HID_FORMAT.format(hid=obj.post.hid)
        )
    admin_post_hid.short_description = 'Post'
    admin_post_hid.admin_order_field = 'post__hid'

    def admin_thread_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_thread_change', args=(obj.post.thread.id,)),
            config.THREAD_HID_FORMAT.format(hid=obj.post.thread.hid)
        )
    admin_thread_hid.short_description = 'Thread'
    admin_thread_hid.admin_order_field = 'post__thread__hid'

    def admin_board_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_board_change', args=(obj.post.thread.board.id,)),
            obj.post.thread.board.hid
        )
    admin_board_hid.short_description = 'Board'
    admin_board_hid.admin_order_field = 'post__thread__board__hid'

    def thumbnail(self, obj):
        if obj.file and obj.thumb_file:
            return format_html(
                '<a href="{}">'
                '<img src={} alt={} title={} style="max-width: 100px; max-height: 100px;" />'
                '</a>',
                ''.join([settings.MEDIA_URL, obj.file.url]),
                ''.join([settings.MEDIA_URL, obj.thumb_file.url]),
                obj.hid(),
                obj.original_name,
            )
    thumbnail.short_description = 'Thumbnail'

    def url(self, obj):
        url = ''.join([settings.MEDIA_URL, obj.file.url])
        return format_html('<a href="{}">{}</a>', url, url)
    url.short_description = 'URL'
