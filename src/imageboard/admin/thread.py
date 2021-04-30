from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count

from ..models import Thread, Post
from hexchan import config


class OpPostInlineAdmin(admin.StackedInline):
    model = Post

    extra = 0

    fields = (
        'title', 'author', 'text', 'images_num', 'ip_address', 'created_by',
    )

    readonly_fields = (
        'title', 'author', 'text', 'images_num', 'ip_address', 'created_by',
    )

    show_change_link = True

    verbose_name = 'OP post'

    verbose_name_plural = 'OP post'

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_op=True).annotate(images_num=Count('images'))

    # Custom fields
    # ==================================================================================================================
    def images_num(self, obj):
        return obj.images_num
    images_num.short_description = 'Images'


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):

    # List options
    # ==================================================================================================================
    list_display = ('id', 'admin_board_hid', 'admin_thread_hid',
                    'posts_num', 'max_posts_num',
                    'is_sticky', 'is_locked', 'is_deleted',
                    'created_at', 'updated_at',
                    )

    list_editable = ('is_sticky', 'is_locked', 'is_deleted',)

    list_filter = ('board', 'created_at', 'is_sticky', 'is_locked', 'is_deleted',)

    list_display_links = (
        'id',
        # 'admin_thread_hid',
    )

    list_per_page = 100

    ordering = ()

    preserve_filters = True

    # Editor options
    # ==================================================================================================================
    inlines = [
        OpPostInlineAdmin
    ]

    readonly_fields = (
        'id',
        'admin_board_hid',  # TODO: Move thread between boards, moved flag
        'admin_thread_hid',
        'created_at',
        'updated_at',
        'posts_num',
    )

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                ('id', 'admin_board_hid', 'admin_thread_hid',),
                ('created_at', 'updated_at',),
            ),
        }),

        ('Post number', {
            'fields': (
                ('posts_num', 'max_posts_num',),
            ),
        }),

        ('Flags', {
            'fields': (
                ('is_sticky', 'is_locked', 'is_deleted',),
            ),
        }),
    )

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('board').annotate(posts_num=Count('posts'))

    # Custom fields
    # ==================================================================================================================
    def admin_board_hid(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:imageboard_board_change', args=(obj.board.id,)),
            obj.board.hid
        )
    admin_board_hid.short_description = 'Board'
    admin_board_hid.admin_order_field = 'board__hid'

    def admin_thread_hid(self, obj):
        return config.THREAD_HID_FORMAT.format(hid=obj.hid)
    admin_thread_hid.short_description = 'HID'
    admin_thread_hid.admin_order_field = 'hid'

    def posts_num(self, obj):
        return obj.posts_num
    posts_num.short_description = 'Posts'
