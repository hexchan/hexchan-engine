# Standard imports
import datetime
from typing import List

# Django imports
from django.http import Http404
from django.core.cache import cache
from django.db.models import Prefetch

# App imports
from hexchan import config
from imageboard.models import Board, Thread, Post


def get_session_list(request, session_key: str, limit=16) -> List[int]:
    return request.session.get(session_key, [])[-limit:]


def push_to_session_list(request, session_key: str, value: int, limit=16) -> None:
    session_list = request.session.get(session_key, [])[-(limit-1):]
    if value not in session_list:
        session_list.append(value)
        request.session[session_key] = session_list


def get_boards():
    """Get all boards."""
    return Board.objects.order_by('hid').filter(is_deleted=False, is_hidden=False)


def get_board(board_hid: str):
    """Get current board."""
    try:
        return Board.objects.get(hid=board_hid, is_deleted=False)
    except Board.DoesNotExist:
        raise Http404('Board not found')


def get_thread(board_hid: str, thread_hid: str):
    """Thread queryset."""
    try:
        return Thread.objects.get(board__hid=board_hid, hid=thread_hid, is_deleted=False)
    except Thread.DoesNotExist:
        raise Http404('Thread not found')


class CacheInterface:
    def __init__(self, key: str, obj, is_admin: bool):
        self.key = key
        self.obj = obj
        self.is_admin = is_admin

    def get_cached_template(self):
        """Get cached page if exists and return it."""
        if config.CACHE_ENABLED and not self.is_admin:
            cache_record = cache.get(self.key)
            if cache_record is not None:
                timestamp, rendered_template = cache_record
                if self.obj.updated_at == timestamp:
                    return rendered_template

    def write_template_to_cache(self, rendered_template: str):
        """Write page to cache."""
        if config.CACHE_ENABLED and not self.is_admin:
            new_cache_record = (self.obj.updated_at, rendered_template,)
            cache.set(self.key, new_cache_record)

    def make_cache_info(self, **kwargs):
        """Make cache info for use in template."""
        if config.CACHE_ENABLED and not self.is_admin:
            cache_data = {
                'updated_at': self.obj.updated_at,
                'generated_at': datetime.datetime.now(),
            }
            cache_data.update(kwargs)
            return cache_data


def prefetch_posts_related_data(posts_field=None, posts_queryset=None):
    """Prefetch related posts with images, authors and replies."""

    # If posts relation field is specified fetch posts with it.
    # Also set it as prefix for additional object prefetches.
    if posts_field is not None:
        prefix = '{}__'.format(posts_field)
        result = [
            Prefetch(posts_field, queryset=posts_queryset)
        ]
    else:
        prefix = ''
        result = []

    refs_and_replies_queryset = Post.objects \
        .select_related('thread', 'thread__board') \
        .only('is_op', 'hid', 'thread__hid', 'thread__board__hid')

    result += [
        Prefetch('{}images'.format(prefix)),
        Prefetch(
            '{}refs'.format(prefix),
            queryset=refs_and_replies_queryset
        ),
        Prefetch(
            '{}post_set'.format(prefix),
            queryset=refs_and_replies_queryset,
            to_attr='replies'
        ),
        Prefetch('{}created_by'.format(prefix))
    ]

    return result
