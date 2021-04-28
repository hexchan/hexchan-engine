from django.db import models
from django.utils.translation import gettext_lazy as _


class Captcha(models.Model):
    solution = models.CharField(
        _('Solution'),
        max_length=32,
        editable=False,
    )

    image = models.BinaryField(
        _('Encoded image'),
        editable=False,
    )

    ip_address = models.CharField(
        _('IP address'),
        max_length=16,
        editable=False,
        db_index=True
    )

    board = models.ForeignKey(
        'Board',
        verbose_name=_('Board'),
        on_delete=models.CASCADE,
        editable=False,
        db_index=True
    )

    thread = models.ForeignKey(
        'Thread',
        verbose_name=_('Thread'),
        on_delete=models.CASCADE,
        editable=False,
        db_index=True,
        null=True,
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False,
        db_index=True
    )

    class Meta:
        verbose_name = _('Captcha')
        verbose_name_plural = _('Captchas')
