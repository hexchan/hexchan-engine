# Standard imports
import ipaddress
import re

# Django imports
from django.utils import timezone
from django.db.models import Q

# App imports
from moderation.models import Ban, WordFilter, ImageFilter
from moderation.exceptions import Banned, BadMessage, BadImage

from imageboard.utils.get_client_ip import get_client_ip


def check_bans(request):
    session_id = request.session.session_key
    client_ip = get_client_ip(request)
    ip = ipaddress.IPv4Address(client_ip)
    net_1 = ipaddress.IPv4Network((ip, 24), strict=False)
    net_2 = ipaddress.IPv4Network((ip, 16), strict=False)
    moment = timezone.now()

    active_bans = Ban.objects.filter(
        Q(type=Ban.BAN_TYPE_IP, value=str(ip)) |
        Q(type=Ban.BAN_TYPE_NET, value=str(net_1)) |
        Q(type=Ban.BAN_TYPE_NET, value=str(net_2)) |
        Q(type=Ban.BAN_TYPE_SESSION, value=session_id),
        active_until__gte=moment
    ).order_by('-created_at')

    if active_bans:
        latest_ban = active_bans[0]

        raise Banned(latest_ban.reason.description, latest_ban.active_until)


def check_text(text):
    filter_expressions = list(WordFilter.objects.values_list('expression', flat=True).all())
    if not filter_expressions:
        return

    combined_re = re.compile('|'.join(filter_expressions))

    matches = combined_re.findall(text)
    if matches:
        raise BadMessage


def check_image(checksum, size):
    banned_images_num = ImageFilter.objects.filter(checksum=checksum, size=size).count()
    if banned_images_num > 0:
        raise BadImage
