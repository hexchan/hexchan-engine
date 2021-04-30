import os.path

from django.db import models
from django.utils.translation import gettext_lazy as _

from hexchan import config


def make_file_upload_path(instance, filename):
    return os.path.join('images', instance.make_file_name())


def make_thumb_file_upload_path(instance, filename):
    return os.path.join('thumbs', instance.make_thumb_file_name())


class Image(models.Model):
    post = models.ForeignKey(
        'Post',
        verbose_name=_('Post'),
        related_name='images',
        on_delete=models.CASCADE,
        db_index=True
    )

    file = models.ImageField(
        _('Image'),
        upload_to=make_file_upload_path,
        width_field='width',
        height_field='height',
        editable=False,
        blank=True,
    )

    original_name = models.CharField(
        _('Original name'),
        max_length=128,
        editable=False
    )

    mimetype = models.CharField(
        _('MIME type'),
        max_length=16,
        editable=False
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    size = models.IntegerField(
        _('Size'),
        editable=False
    )

    width = models.IntegerField(
        _('Width'),
        editable=False,
        blank=True,
        null=True,
    )

    height = models.IntegerField(
        _('Height'),
        editable=False,
        blank=True,
        null=True,
    )

    is_spoiler = models.BooleanField(
        _('Is spoiler'),
        default=False,
    )

    is_deleted = models.BooleanField(
        _('Is deleted'),
        default=False,
        db_index=True
    )

    checksum = models.CharField(
        _('Checksum'),
        max_length=32,
        editable=False,
        blank=True
    )

    thumb_file = models.ImageField(
        _('Thumb'),
        upload_to=make_thumb_file_upload_path,
        width_field='thumb_width',
        height_field='thumb_height',
        editable=False,
        blank=True,
    )

    thumb_width = models.IntegerField(
        _('Thumb width'),
        editable=False,
        blank=True,
        null=True,
    )

    thumb_height = models.IntegerField(
        _('Thumb height'),
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        unique_together = []
        indexes = []
        ordering = ['id']

    def hid(self):
        return config.IMAGE_HID_FORMAT.format(hid=self.id) if self.id is not None else None

    def make_file_name(self):
        return '{name}.{ext}'.format(
            name=self.hid(),
            ext=config.IMAGE_EXTENSION[self.mimetype]
        )

    def make_thumb_file_name(self):
        return '{name}.{ext}'.format(
            name=self.hid(),
            ext=config.THUMB_EXTENSION
        )

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        self.delete_files()

    def delete_files(self):
        os.remove(self.file.path)
        os.remove(self.thumb_file.path)
