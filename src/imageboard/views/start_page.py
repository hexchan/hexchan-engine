# Django imports
from django.db.models import Prefetch, OuterRef, Subquery
from django.views.generic import TemplateView

# App imports
from imageboard.models import Board, Thread, ContentBlock


class StartPage(TemplateView):
    template_name = 'imageboard/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recently updated threads queryset
        updated_threads_queryset = (
            Thread.objects
                  .filter(board=OuterRef('board'), is_deleted=False)
                  .order_by('-is_sticky', '-updated_at')
                  .values_list('id', flat=True)[:5]
        )

        # Prefetch threads
        threads_prefetch = Prefetch(
            'threads',
            queryset=(
                Thread.objects_with_op
                      .filter(id__in=Subquery(updated_threads_queryset))
                      .order_by('-is_sticky', '-updated_at')
            ),
            to_attr='updated_threads'
        )

        # Get boards with threads and OP posts
        context['boards'] = Board.active_objects.prefetch_related(threads_prefetch)

        # Get index page content
        context['index_page_text'] = ContentBlock.objects.get(is_active=True, hid='index_page_text')

        return context
