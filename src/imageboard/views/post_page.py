# Django imports
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

# App imports
from imageboard.models import Board, Post


class PostPage(TemplateView):
    template_name = 'imageboard/post_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board_hid = self.kwargs['board_hid']
        thread_hid = self.kwargs['thread_hid']
        post_hid = self.kwargs['post_hid']

        board = get_object_or_404(Board, hid=board_hid, is_deleted=False)

        # Don't use get_object_or_404 for getting post to simplify frontend
        try:
            post = Post.posts.get(hid=post_hid, thread__hid=thread_hid, thread__board__hid=board_hid)
        except Post.DoesNotExist:
            post = None

        context.update({
            'board': board,
            'post': post,
            'is_popup': True,
        })

        return context
