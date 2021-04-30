# Django imports
from django.db.models import Prefetch
from django.views.generic import TemplateView

# App imports
from imageboard.models import Board, Thread, Post, ContentBlock


class StartPage(TemplateView):
    template_name = 'imageboard/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get boards with threads and OP posts
        context['boards'] = Board.active_objects.prefetch_related(
            Prefetch(
                'threads',
                queryset=(
                    Thread.threads.filter_last_updated().prefetch_related(
                        Prefetch(
                            'op',
                            queryset=Post.posts.filter_op()
                        )
                    )
                )
            )
        )

        # Get index page content
        context['index_page_text'] = ContentBlock.objects.get(is_active=True, hid='index_page_text')

        return context
