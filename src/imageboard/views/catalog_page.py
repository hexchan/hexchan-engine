# Django imports
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# App imports
from imageboard.models import Board, Thread
from imageboard.views import parts


def catalog_page(request, board_hid):
    # Create response object
    response = HttpResponse()

    # Get boards
    boards = parts.get_boards()

    # Get current board
    board = get_object_or_404(Board, hid=board_hid)

    threads = Thread.objects_with_op.filter(board=board).order_by('-is_sticky', '-updated_at')[:board.max_threads_num]

    # Render template
    rendered_template = render_to_string(
        'imageboard/catalog_page.html',
        {
            'board': board,
            'boards': boards,
            'threads': threads,
        },
        request,
    )

    # Return response
    response.write(rendered_template)
    return response
