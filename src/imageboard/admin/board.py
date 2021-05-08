from django.contrib import admin
from django.db.models import Count

from ..models import Board
from hexchan import config


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    # List options
    # ==================================================================================================================
    list_display = (
        'id', 'hid',
        'name', 'threads_num', 'default_username',
        'default_max_posts_num', 'admin_last_post_hid',
        'is_hidden', 'is_locked', 'is_deleted',
        'created_at', 'updated_at',
    )

    list_editable = (
        'is_hidden', 'is_locked', 'is_deleted',
    )

    # Editor options
    # ==================================================================================================================
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'admin_last_post_hid',
        'threads_num',
    )

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'hid',
                'name',
                ('created_at', 'updated_at',),
                ('threads_num', 'admin_last_post_hid',),
            ),
        }),

        ('About board', {
            'fields': (
                'description', 'keywords', 'rules', 'custom_style',
            ),
        }),

        ('Parameters', {
            'fields': (
                'posts_per_thread_per_page', 'threads_per_page', 'max_threads_num',
            )
        }),

        ('Defaults', {
            'fields': (
                'default_username',
                'default_max_posts_num',
            ),
        }),

        ('Flags', {
            'fields': (
                ('is_hidden', 'is_locked', 'is_deleted',),
            ),
        }),
    )

    # Modified main queryset (prefetch some related stuff)
    # ==================================================================================================================
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(threads_num=Count('threads'))

    # Custom fields
    # ==================================================================================================================
    def threads_num(self, obj):
        return obj.threads_num
    threads_num.short_description = 'Threads'

    def admin_last_post_hid(self, obj):
        return config.THREAD_HID_FORMAT.format(hid=obj.last_post_hid) if obj.last_post_hid else None
    admin_last_post_hid.short_description = 'Last post HID'
