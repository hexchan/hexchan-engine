from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImageboardConfig(AppConfig):
    name = 'imageboard'
    verbose_name = _('Imageboard')
