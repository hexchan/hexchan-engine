# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm
from imageboard.views import parts


def thread_page(request, board_hid, thread_hid):
    # Create response object
    response = HttpResponse()

    # Send some user session data as cookies
    parts.set_session_data_as_cookie(request, response, 'user_threads')
    parts.set_session_data_as_cookie(request, response, 'user_posts')
    parts.set_session_data_as_cookie(request, response, 'user_thread_replies')

    # Get boards
    boards = parts.get_boards()

    # Get current board
    board = get_object_or_404(Board, hid=board_hid)

    # Prefetch stuff for the thread
    thread = Thread.objects\
        .select_related('board')\
        .prefetch_related(Prefetch('posts', queryset=Post.active_objects.all()))\
        .annotate(posts_count=Count('posts')) \
        .get(board__hid=board_hid, hid=thread_hid, is_deleted=False)

    # Add extra data
    thread.other_posts = []
    for post in thread.posts.all():
        if post.is_op:
            thread.op = post
        else:
            thread.other_posts.append(post)

    # Init post creation form
    form = PostingForm(
        initial={
            'form_type': 'new_post',
            'board_id': board.id,
            'thread_id': thread.id,
        },
    )

    # Render template
    rendered_template = render_to_string(
        'imageboard/thread_page.html',
        {
            'page_type': 'thread_page',
            'form': form,
            'board': board,
            'boards': boards,
            'thread': thread,
        },
        request
    )

    response.write(rendered_template)
    return response
