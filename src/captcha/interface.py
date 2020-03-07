import datetime
import random

from captcha.models import Captcha
from captcha import exceptions


def set_captcha(request):
    captcha_ids = Captcha.objects.values_list('pk', flat=True)

    captcha_count = len(captcha_ids)

    if captcha_count == 0:
        raise exceptions.CaptchaDbIsEmpty

    random_id = random.choice(captcha_ids)
    captcha = Captcha.objects.get(pk=random_id)

    # TODO: Move delta to the config
    captcha_expires = (datetime.datetime.now() + datetime.timedelta(minutes=10)).timestamp()

    request.session['captcha_id'] = captcha.id
    request.session['captcha_expires'] = captcha_expires

    return captcha


def get_captcha(request, do_force_update=False):
    captcha_id = request.session.get('captcha_id')
    captcha_expires = request.session.get('captcha_expires')

    # If forced update, captcha info missing in the session or captcha has expired - set a new one...
    if (
        do_force_update or
        captcha_id is None or
        captcha_expires is None or
        datetime.datetime.fromtimestamp(captcha_expires) < datetime.datetime.now()
    ):
        captcha = set_captcha(request)
    # ...or else get captcha object from DB by session-stored ID
    else:
        try:
            captcha = Captcha.objects.get(pk=captcha_id)
        except Captcha.DoesNotExist:
            raise exceptions.CaptchaNotFound

    return captcha


def check_captcha(request, public_id, solution):
    captcha_id = request.session.get('captcha_id')
    captcha_expires = request.session.get('captcha_expires')

    # Get captcha object from DB by session-stored ID
    try:
        captcha = Captcha.objects.get(pk=captcha_id)
    except Captcha.DoesNotExist:
        raise exceptions.CaptchaNotFound

    # Check if captcha in session has expired
    if datetime.datetime.fromtimestamp(captcha_expires) < datetime.datetime.now():
        raise exceptions.CaptchaHasExpired

    # Check if user responses to correct captcha
    if public_id != captcha.public_id:
        raise exceptions.CaptchaHasExpired

    # Check user response value (case insensitive)
    if solution.lower() != captcha.solution.lower():
        raise exceptions.CaptchaIsInvalid
