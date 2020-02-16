from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings

from ..models import Post, Image
from hexchan import config


class ImageInlineAdmin(admin.TabularInline):
    model = Image

    extra = 0

    fields = (
        'hid', 'thumbnail', 'file', 'original_name', 'mimetype', 'created_at', 'size', 'width', 'height', 'checksum',
        'is_spoiler', 'is_deleted',
    )

    readonly_fields = (
        'hid', 'thumbnail', 'file', 'original_name', 'mimetype', 'created_at', 'size', 'width', 'height', 'checksum',
    )

    show_change_link = True

    # # Custom fields
    # # ==================================================================================================================
    def thumbnail(self, obj):
        return format_html(
            '<a href="{}">'
            '<img src={} alt={} title={} style="max-width: 100px; max-height: 100px;" />'
            '</a>',
            str(obj.file.url),
            str(obj.thumb_file.url),
            obj.hid(),
            obj.original_name,
        )
    thumbnail.short_description = 'Thumbnail'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # List options
    # ==================================================================================================================
    list_display = ('id', 'admin_board_hid', 'admin_thread_hid', 'admin_post_hid', 'is_op',
                    'author', 'images_num', 'ip_address',
                    'user_was_warned', 'user_was_banned', 'is_deleted',
                    'created_at', 'updated_at',
                    )

    list_editable = ('user_was_warned', 'user_was_banned', 'is_deleted',)

    list_filter = ('is_deleted', 'created_at', 'thread__board', 'is_op', 'created_by')

    list_display_links = (
        # 'admin_full_hid',
        'id',
        # 'admin_post_hid',
    )

    list_per_page = 100

    ordering = ('-id',)

    preserve_filters = True

    # Editor options
    # ==================================================================================================================
    inlines = [
        ImageInlineAdmin,
    ]

    readonly_fields = (
        'admin_board_hid',
        'admin_thread_hid',
        'admin_post_hid',
        'created_at',
        'updated_at',
        'id',
        'created_by',
        'ip_address',
        'is_op',
        'session_id',
    )

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                ('id', 'admin_board_hid', 'admin_thread_hid', 'admin_post_hid', 'is_op'),
                ('created_at', 'updated_at',),
                ('created_by', 'ip_address', 'session_id'),
            ),
        }),

        ('Content', {
            'fields': (
                'title',
                'author',
                'text',
                'email',
                'password',
            ),
        }),

        ('Flags', {
            'fields': (
                (
                    'is_deleted',
                    'user_was_warned',
                    'user_was_banned',
                ),
            ),
        }),
    )

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('thread', 'thread__board', 'images')

    # Custom fields
    # ==================================================================================================================
    def admin_post_hid(self, obj):
        return config.POST_HID_FORMAT.format(hid=obj.hid)
    admin_post_hid.short_description = 'HID'
    admin_post_hid.admin_order_field = 'hid'

    def admin_thread_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_thread_change', args=(obj.thread.id,)),
            config.THREAD_HID_FORMAT.format(hid=obj.thread.hid)
        )
    admin_thread_hid.short_description = 'Thread'
    admin_thread_hid.admin_order_field = 'thread__hid'

    def admin_board_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_board_change', args=(obj.thread.board.id,)),
            obj.thread.board.hid
        )
    admin_board_hid.short_description = 'Board'
    admin_board_hid.admin_order_field = 'thread__board__hid'

    def images_num(self, obj):
        return obj.images.count()
    images_num.short_description = 'Images'

    def post_modified(self, obj):
        return obj.updated_at and obj.updated_at != obj.created_at
    post_modified.short_description = 'Modified'
    post_modified.boolean = True

    def content(self, obj):
        content = ''
        if obj.title:
            content += obj.title
        if obj.text:
            content += obj.text
        return content[:64]
    content.short_description = 'Content'
