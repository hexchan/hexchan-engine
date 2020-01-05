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

    # Get boards
    boards = parts.get_boards()

    # Get current board
    board = get_object_or_404(Board, hid=board_hid)

    # Prefetch stuff for the thread
    thread = Thread.objects_with_op\
        .select_related('board')\
        .prefetch_related(Prefetch('posts', queryset=Post.active_objects.filter(is_op=False), to_attr='other_posts'))\
        .get(board__hid=board_hid, hid=thread_hid)

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
