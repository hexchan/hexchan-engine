# Django imports
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm


class ThreadPage(TemplateView):
    template_name = 'imageboard/thread_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board_hid = self.kwargs['board_hid']
        thread_hid = self.kwargs['thread_hid']

        boards = Board.active_objects.all()

        board = get_object_or_404(Board, hid=board_hid)

        other_posts_prefetch = Prefetch('posts', queryset=Post.active_objects.filter(is_op=False), to_attr='other_posts')

        thread = get_object_or_404(
            Thread.objects_with_op.prefetch_related(other_posts_prefetch),
            board__hid=board_hid,
            hid=thread_hid,
        )

        form = PostingForm(
            initial={
                'form_type': 'new_post',
                'board_id': board.id,
                'thread_id': thread.id,
            },
        )

        context.update({
            'page_type': 'thread_page',
            'form': form,
            'board': board,
            'boards': boards,
            'thread': thread,
        })

        return context
