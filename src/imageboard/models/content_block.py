from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentBlock(models.Model):
    hid = models.CharField(
        _('HID'),
        editable=True,
        db_index=True,
        unique=True,
        max_length=32,
    )

    text = models.TextField(
        _('Text'),
        blank=True
    )

    is_active = models.BooleanField(
        _('Is active'),
        default=False,
        db_index=True
    )

    class Meta:
        verbose_name = _('Content block')
        verbose_name_plural = _('Content blocks')
