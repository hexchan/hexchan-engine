# Django imports
from django.http import HttpResponse

# App imports
from imageboard.models import Captcha
from imageboard.utils.get_client_ip import get_client_ip
from imageboard.utils.captchamaker import make_word, draw_single_captcha, image_to_bytes


def captcha_view(request):
    board_id = request.GET.get('board')
    thread_id = request.GET.get('thread')
    client_ip = get_client_ip(request)

    try:
        captcha = Captcha.objects.get(
            board_id=board_id,
            thread_id=thread_id,
            ip_address=client_ip,
        )
        
    except Captcha.DoesNotExist:
        solution = make_word().upper()
        image = draw_single_captcha(solution)
        image_bytes = image_to_bytes(image)

        captcha = Captcha.objects.create(
            board_id=board_id,
            thread_id=thread_id,
            ip_address=client_ip,
            solution=solution,
            image=image_bytes
        )

    return HttpResponse(captcha.image, content_type='image/png')
