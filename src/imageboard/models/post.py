from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch, F
from django.utils.functional import cached_property

from hexchan import config


class RefReplyManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                .select_related('thread', 'thread__board')
                .only('is_op', 'hid', 'thread__hid', 'thread__board__hid')
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                .filter(is_deleted=False)
                .select_related('thread', 'thread__board')
                .prefetch_related(
                    Prefetch('images'),
                    Prefetch('refs', queryset=Post.ref_and_reply_objects.all()),
                    Prefetch('post_set', to_attr='replies', queryset=Post.ref_and_reply_objects.all()),
                    Prefetch('created_by'),
                )
                .annotate(
                    thread_hid=F('thread__hid'),
                    board_hid=F('thread__board__hid'),
                )
        )


class Post(models.Model):
    hid = models.IntegerField(
        _('HID'),
        editable=False,
        db_index=True
    )

    thread = models.ForeignKey(
        'Thread',
        verbose_name=_('Thread'),
        related_name='posts',
        on_delete=models.CASCADE,
        editable=False,
        db_index=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False,
        db_index=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        editable=False,
        db_index=True
    )

    text = models.TextField(
        _('Text'),
        max_length=2048,
        blank=True
    )

    title = models.CharField(
        _('Title'),
        max_length=64,
        blank=True
    )

    author = models.CharField(
        _('Author'),
        max_length=32,
        blank=True
    )

    email = models.CharField(
        _('E-mail'),
        max_length=32,
        blank=True
    )

    password = models.CharField(
        _('Password'),
        max_length=16,
        blank=True
    )

    is_op = models.BooleanField(
        _('Is OP'),
        editable=False
    )

    user_was_warned = models.BooleanField(
        _('User was warned'),
        default=False
    )

    user_was_banned = models.BooleanField(
        _('User was banned'),
        default=False
    )

    is_deleted = models.BooleanField(
        _('Is deleted'),
        default=False,
        db_index=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Created by'),
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    refs = models.ManyToManyField(
        'self',
        verbose_name=_('Refs'),
        editable=False,
        db_index=True,
        symmetrical=False
    )

    ip_address = models.CharField(
        _('IP address'),
        max_length=16,
        editable=False,
        db_index=True
    )

    session_id = models.CharField(
        _('Session ID'),
        max_length=32,
        editable=False,
        db_index=True
    )

    objects = models.Manager()

    active_objects = PostManager()

    ref_and_reply_objects = RefReplyManager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        unique_together = ['thread', 'hid']
        indexes = []
        ordering = ['id']

    def hid2hex(self):
        return config.POST_FULL_HID_FORMAT.format(hid=self.hid)

    def get_absolute_url(self):
        thread_url = reverse(
            'thread_page',
            kwargs={'board_hid': self.thread.board.hid, 'thread_hid': self.thread.hid}
        )

        post_url = '{thread_url}#{post_hid}'.format(
            thread_url=thread_url,
            post_hid=self.hid2hex()
        )

        return post_url

    @cached_property
    def ref_urls(self):
        return {ref.hid: ref.get_absolute_url() for ref in self.refs.all()}
