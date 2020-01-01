# Django imports
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Prefetch, OuterRef, Subquery, Q

# App imports
from imageboard.models import Board, Thread
from imageboard.views.parts import set_session_data_as_cookie


def start_page(request):
    # Create response object
    response = HttpResponse()

    # Recently updated threads queryset
    updated_threads_queryset = Thread.objects\
        .filter(board=OuterRef('board'), is_deleted=False)\
        .order_by('-is_sticky', '-updated_at')\
        .values_list('id', flat=True)[:5]

    # Prefetch threads
    threads_prefetch = Prefetch(
        'threads',
        queryset=Thread.objects_with_op
                       .filter(id__in=Subquery(updated_threads_queryset))
                       .order_by('-is_sticky', '-updated_at'),
        to_attr='updated_threads'
    )

    # Get boards with threads and OP posts
    boards = Board.objects\
        .order_by('hid')\
        .filter(is_deleted=False, is_hidden=False)\
        .prefetch_related(threads_prefetch)

    rendered_template = render_to_string(
        'imageboard/start_page.html',
        {
            'boards': boards,
        },
        request
    )

    response.write(rendered_template)
    return response
