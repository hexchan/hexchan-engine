# Django imports
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

# App imports
from imageboard.models import Board, Thread, Post


class CatalogPage(TemplateView):
    template_name = 'imageboard/catalog_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board_hid = self.kwargs['board_hid']

        boards = Board.active_objects.all()

        # Get current board
        board = get_object_or_404(Board, hid=board_hid)

        threads = (
            Thread.threads
            .prefetch_related(
                Prefetch(
                    'op',
                    queryset=Post.posts.filter_op()
                )
            )
            .filter(
                board=board
            )
            .order_by('-is_sticky', '-updated_at')
            [:board.max_threads_num]
        )

        context.update({
            'board': board,
            'boards': boards,
            'threads': threads,
        })

        return context
