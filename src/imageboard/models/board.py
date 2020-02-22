from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BoardManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().order_by('hid').filter(is_deleted=False, is_hidden=False)
        )


class Board(models.Model):
    hid = models.CharField(
        _('HID'),
        max_length=8,
        db_index=True
    )

    name = models.CharField(
        _('Name'),
        max_length=64
    )

    description = models.CharField(
        _('Description'),
        help_text=_('Short board description'),
        max_length=256,
        blank=True
    )

    rules = models.TextField(
        _('Rules'),
        help_text=_('Board rules will be displayed next to posting form.'),
        blank=True
    )

    custom_style = models.TextField(
        _('Custom style'),
        help_text=_('Custom CSS that would be applied only on this board\'s pages'),
        blank=True
    )

    default_username = models.CharField(
        _('Default username'),
        help_text=_('Default username will be saved, if post\'s author field was empty.'),
        max_length=32
    )

    default_max_posts_num = models.IntegerField(
        _('Default maximum posts number'),
        help_text=_('Maximum number of posts for new threads by default. Can be overridden in thread\'s properties.'),
        default=128
    )

    posts_per_thread_per_page = models.IntegerField(
        _('Posts per thread per page'),
        help_text=_('Number of thread\'s posts visible on board\'s pages, not counting OP post.'),
        default=5
    )

    threads_per_page = models.IntegerField(
        _('Threads per page'),
        help_text=_('Number of threads on board\'s page'),
        default=10
    )

    max_threads_num = models.IntegerField(
        _('Maximum threads number'),
        help_text=_('Maximum number of threads on this boards. When reaching this level older threads will be deleted.'),
        default=100
    )

    is_hidden = models.BooleanField(
        _('Is hidden'),
        help_text=_('Is this board hidden from boards list. Can still be accessed by direct URL.'),
        default=False
    )

    is_locked = models.BooleanField(
        _('Is locked'),
        help_text=_('New posts and threads can\'t be created on locked board.'),
        default=False
    )

    is_deleted = models.BooleanField(
        _('Is deleted'),
        help_text=_('Boards is removed from boards list and can\'t be accessed by direct URL.'),
        default=False
    )

    last_post_hid = models.IntegerField(
        _('Last post HID'),
        null=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        editable=False
    )

    objects = models.Manager()

    active_objects = BoardManager()

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')
        ordering = ['hid']

    def __str__(self):
        return self.hid

    def threads_count(self):
        return self.threads.count()

    def get_absolute_url(self):
        return reverse('board_page', kwargs={'board_hid': self.hid})
