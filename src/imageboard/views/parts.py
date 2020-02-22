# Django imports
from django.http import HttpRequest

# Standard imports
from typing import List


def get_session_list(request: HttpRequest, session_key: str, limit=16) -> List[int]:
    return request.session.get(session_key, [])[-limit:]


def push_to_session_list(request: HttpRequest, session_key: str, value: int, limit=16) -> None:
    session_list = request.session.get(session_key, [])[-(limit-1):]
    if value not in session_list:
        session_list.append(value)
        request.session[session_key] = session_list
