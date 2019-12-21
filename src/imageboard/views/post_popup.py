# Django imports
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404

# App imports
from hexchan import config
from imageboard.models import Board, Post


@cache_page(config.CACHE_POST_POPUP)
def post_popup(request, board_hid, thread_hid, post_hid):
    # Get current board
    board = get_object_or_404(Board, hid=board_hid, is_deleted=False)

    # Get current post
    try:
        post = Post.active_objects.get(hid=post_hid, thread__hid=thread_hid, thread__board__hid=board_hid)
    except Post.DoesNotExist:
        post = None

    # Render template
    rendered_template = render_to_string(
        'imageboard/post_popup.html',
        {
            'board': board,
            'post': post,
            'is_popup': True,
        },
        request,
    )

    # Return response
    return HttpResponse(rendered_template)
