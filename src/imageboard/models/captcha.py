from django.db import models
from django.utils.translation import gettext_lazy as _


class Captcha(models.Model):
    public_id = models.CharField(
        _('Public ID'),
        max_length=32
    )

    solution = models.CharField(
        _('Solution'),
        max_length=32
    )

    image = models.TextField(
        _('Encoded image'),
    )

    class Meta:
        verbose_name = _('Captcha')
        verbose_name_plural = _('Captchas')
