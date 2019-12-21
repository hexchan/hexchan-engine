# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Subquery, OuterRef
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.views import parts
from imageboard.forms import PostingForm


def board_page(request, board_hid, page_num=1):
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

    # Queryset for latest posts
    latest_posts_queryset = Post.objects\
        .filter(thread=OuterRef('thread'), is_deleted=False, is_op=False)\
        .order_by('-id')\
        .values_list('id', flat=True)[:board.posts_per_thread_per_page]

    # Threads queryset
    threads = Thread.objects_with_op\
        .filter(board__hid=board_hid)\
        .prefetch_related(
            Prefetch(
                'posts',
                queryset=Post.active_objects.filter(id__in=Subquery(latest_posts_queryset)),
                to_attr='latest_posts'
            )
        )\
        .order_by('-is_sticky', '-updated_at')[:board.max_threads_num]

    # Paginate threads
    paginator = Paginator(threads, board.threads_per_page)
    paginated_threads = paginator.get_page(page_num)

    # Init thread creation form
    form = PostingForm(
        initial={
            'form_type': 'new_thread',
            'board_id': board.id,
        },
    )

    # Render template
    rendered_template = render_to_string(
        'imageboard/board_page.html',
        {
            'page_type': 'board_page',
            'form': form,
            'board': board,
            'boards': boards,
            'threads': paginated_threads,
            'page': page_num,
        },
        request
    )

    # Return response
    response.write(rendered_template)
    return response
