# Django imports
from django.http import JsonResponse

# App imports
from imageboard.views.parts import get_session_list


def session_data_view(request):
    user_threads = get_session_list(request, 'user_threads')
    user_posts = get_session_list(request, 'user_posts')
    user_thread_replies = get_session_list(request, 'user_thread_replies')
    updated_at = request.session.get('updated_at')

    return JsonResponse({
        'user_threads': user_threads,
        'user_posts': user_posts,
        'user_thread_replies': user_thread_replies,
        'updated_at': updated_at,
    })
