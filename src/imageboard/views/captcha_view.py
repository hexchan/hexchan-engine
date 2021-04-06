# Django imports
from django.http import JsonResponse

# App imports
from imageboard.utils.captcha_interface import get_captcha
from imageboard.exceptions import CaptchaError


def captcha_view(request):
    do_force_update = request.GET.get('update', False)

    try:
        captcha = get_captcha(request, do_force_update)
    except CaptchaError as e:
        return JsonResponse({'status': 'error'}, status=500)

    response_data = {
        'status': 'ok',
        'publicId': captcha.public_id,
        'image': captcha.image,
    }

    return JsonResponse(response_data)
