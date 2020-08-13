# Django imports
from django.db.models import Prefetch, Subquery, OuterRef
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm


class BoardPage(TemplateView):
    template_name = 'imageboard/board_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board_hid = self.kwargs['board_hid']
        page_num = self.kwargs.get('page_num', 1)

        boards = Board.active_objects.all()

        board = get_object_or_404(Board, hid=board_hid)

        # Queryset for latest posts
        latest_posts_queryset = (
            Post.objects
                .filter(thread=OuterRef('thread'), is_deleted=False, is_op=False)
                .order_by('-id')
                .values_list('id', flat=True)[:board.posts_per_thread_per_page]
        )

        # Threads queryset
        threads = (
            Thread.objects_with_op
                .filter(board__hid=board_hid)
                .prefetch_related(
                    Prefetch(
                        'posts',
                        queryset=Post.active_objects.filter(id__in=Subquery(latest_posts_queryset)),
                        to_attr='latest_posts'
                    )
            )
            .order_by('-is_sticky', '-updated_at')[:board.max_threads_num]
        )

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

        context.update({
            'page_type': 'board_page',
            'form': form,
            'board': board,
            'boards': boards,
            'threads': paginated_threads,
            'page': page_num,
        })

        return context
