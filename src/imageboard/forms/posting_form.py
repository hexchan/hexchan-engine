# Standard library imports
import hashlib
import datetime

# Django imports
from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.utils import timezone

# Third party imports
import bleach

# App imports
from imageboard.forms.textarea_widget import TextareaWidget
from imageboard.forms.images_widget import ImagesWidget
from imageboard.forms.captcha_widget import CaptchaField
from imageboard.utils.captcha_interface import check_captcha
from imageboard.models import Board, Thread, Post
import moderation.interface
import moderation.exceptions
from imageboard.exceptions import CaptchaIsInvalid, CaptchaHasExpired
from hexchan import config
from imageboard.utils.get_pretty_file_size import get_pretty_file_size


class PostingForm(forms.ModelForm):
    form_type = forms.CharField(
        widget=forms.HiddenInput
    )

    board_id = forms.IntegerField(
        widget=forms.HiddenInput
    )

    thread_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput
    )

    captcha = CaptchaField(
        label=_('Captcha'), required=True
    )

    images = forms.FileField(
        required=False, label=pgettext_lazy('posting form', 'Images'),
        widget=ImagesWidget()
    )

    ERROR_MISSING_THREAD_ID = 'ERROR_MISSING_THREAD_ID'
    ERROR_MESSAGE_IS_EMPTY = 'ERROR_MESSAGE_IS_EMPTY'
    ERROR_BAD_FORM_TYPE = 'ERROR_BAD_FORM_TYPE'
    ERROR_BOARD_NOT_FOUND = 'ERROR_BOARD_NOT_FOUND'
    ERROR_BOARD_IS_LOCKED = 'ERROR_BOARD_IS_LOCKED'
    ERROR_THREAD_NOT_FOUND = 'ERROR_THREAD_NOT_FOUND'
    ERROR_THREAD_IS_LOCKED = 'ERROR_THREAD_IS_LOCKED'
    ERROR_POST_LIMIT_WAS_REACHED = 'ERROR_POST_LIMIT_WAS_REACHED'
    ERROR_TOO_MANY_FILES = 'ERROR_TOO_MANY_FILES'
    ERROR_FILE_IS_TOO_LARGE = 'ERROR_FILE_IS_TOO_LARGE'
    ERROR_BAD_FILE_TYPE = 'ERROR_BAD_FILE_TYPE'
    ERROR_NOT_SO_FAST = 'ERROR_NOT_SO_FAST'
    ERROR_CAPTCHA_IS_INVALID = 'ERROR_CAPTCHA_IS_INVALID'
    ERROR_CAPTHCA_HAS_EXPIRED = 'ERROR_CAPTHCA_HAS_EXPIRED'
    ERROR_BANNED = 'ERROR_BANNED'
    ERROR_BAD_IMAGE = 'ERROR_BAD_IMAGE'
    ERROR_BAD_MESSAGE = 'ERROR_BAD_MESSAGE'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostingForm, self).__init__(*args, **kwargs)

    field_order = ['author', 'title', 'text', 'images', 'captcha']

    class Meta:
        model = Post
        fields = [
            # Custom form fields:
            'form_type', 'board_id', 'thread_id',
            # Model fields:
            'text', 'title', 'author',
            # More custom form fields:
            'captcha', 'images',
        ]

        widgets = {
            'text': TextareaWidget
        }

        error_messages = {}

    def clean(self):
        cleaned_data = super().clean()

        self._check_if_thread_id_is_missing(cleaned_data)
        self._check_if_message_is_empty(cleaned_data)

        try:
            moderation.interface.check_bans(self.request)
        except moderation.exceptions.Banned:
            raise ValidationError(_('You were banned'), code=self.ERROR_BANNED)

        self._check_posting_limit(self.request)

    def clean_form_type(self):
        form_type = self.cleaned_data.get('form_type')

        if form_type not in ['new_thread', 'new_post']:
            raise forms.ValidationError(_('Incorrect form type'), code=self.ERROR_BAD_FORM_TYPE)

        return form_type

    def clean_board_id(self):
        board_id = self.cleaned_data['board_id']

        try:
            board = Board.objects.select_for_update().get(id=board_id, is_deleted=False)
        except Board.DoesNotExist:
            raise ValidationError(_('Board not found'), code=self.ERROR_BOARD_NOT_FOUND)

        if board.is_locked:
            raise ValidationError(_('Board is locked'), code=self.ERROR_BOARD_IS_LOCKED)

        return board_id

    def clean_thread_id(self):
        thread_id = self.cleaned_data['thread_id']

        if thread_id is not None:
            try:
                thread = Thread.objects.select_for_update().get(id=thread_id, is_deleted=False)
            except Thread.DoesNotExist:
                raise ValidationError(_('Thread not found'), code=self.ERROR_THREAD_NOT_FOUND)

            if thread.is_locked:
                raise ValidationError(_('Thread is locked'), code=self.ERROR_THREAD_IS_LOCKED)

            if thread.posts.count() >= thread.max_posts_num:
                raise ValidationError(_('Post limit was reached'), code=self.ERROR_POST_LIMIT_WAS_REACHED)

        return thread_id

    def clean_captcha(self):
        captcha = self.cleaned_data['captcha']

        captcha_public_id = captcha.get('public_id')
        captcha_solution = captcha.get('solution')

        if self.request.user.is_authenticated:
            pass
        else:
            try:
                check_captcha(self.request, captcha_public_id, captcha_solution)

            except CaptchaIsInvalid:
                raise ValidationError(_('Captcha is invalid'), code=self.ERROR_CAPTCHA_IS_INVALID)

            except CaptchaHasExpired:
                raise ValidationError(_('Captcha has expired'), code=self.ERROR_CAPTHCA_HAS_EXPIRED)

        return captcha

    def clean_text(self):
        text = self.cleaned_data['text']

        try:
            moderation.interface.check_text(text)
        except moderation.exceptions.BadMessage:
            raise ValidationError(_('Text rejected'), code=self.ERROR_BAD_MESSAGE)

        return bleach.clean(text)

    def clean_author(self):
        return bleach.clean(self.cleaned_data['author'])

    def clean_title(self):
        return bleach.clean(self.cleaned_data['title'])

    def clean_images(self):
        images = self.files.getlist('images')

        # Check number of images
        self._check_number_of_images(images)

        # Check every image
        for image in images:
            self._check_image_size(image)
            self._check_image_type(image)
            self._attach_checksum_to_image(image)

            try:
                moderation.interface.check_image(image.md5_checksum, image.size)
            except moderation.exceptions.BadImage:
                raise ValidationError(_('Image rejected'), code=self.ERROR_BAD_IMAGE)

        return images

    def _check_posting_limit(self, request):
        latest_post_at = request.session.get('latest_post_at')
        if latest_post_at:
            latest_post_at_datetime = datetime.datetime.fromtimestamp(latest_post_at, tz=timezone.utc)
            now = timezone.now()
            timeout = datetime.timedelta(seconds=config.POSTING_TIMEOUT)
            if (now - latest_post_at_datetime) < timeout:
                raise ValidationError(
                    _('You have to wait for about %(timeout)s seconds to post again.'),
                    code=self.ERROR_NOT_SO_FAST,
                    params={'timeout': config.POSTING_TIMEOUT}
                )

    def _check_number_of_images(self, images):
        if len(images) > config.FILE_MAX_NUM:
            raise ValidationError(
                _('Too many files attached, up to %(max_files)s file(s) are allowed'),
                code=self.ERROR_TOO_MANY_FILES,
                params={'max_files': config.FILE_MAX_NUM}
            )

    def _check_image_size(self, image):
        if image.size > config.FILE_MAX_SIZE:
            raise ValidationError(
                _('Attached file size is too large, sizes up to %(file_size)s are allowed'),
                code=self.ERROR_FILE_IS_TOO_LARGE,
                params={'file_size': get_pretty_file_size(config.FILE_MAX_SIZE)}
            )

    def _check_image_type(self, image):
        if image.content_type not in config.FILE_MIME_TYPES:
            raise ValidationError(
                _('Attached file has an unsupported type, only types %(types)s are supported'),
                code=self.ERROR_BAD_FILE_TYPE,
                params={'types': ', '.join(config.FILE_MIME_TYPES)}
            )

    def _attach_checksum_to_image(self, image):
        """Calculate checksum and add it to the image object."""

        checksum_obj = hashlib.md5()
        for chunk in image.chunks(config.IMAGE_CHUNK_SIZE):
            checksum_obj.update(chunk)
        image.md5_checksum = checksum_obj.hexdigest()

    def _check_if_message_is_empty(self, cleaned_data):
        text = cleaned_data.get('text')
        images = cleaned_data.get('images')
        if not text and not images:
            raise ValidationError(
                _('Message should not be empty, either write some text or attach an image'),
                code=self.ERROR_MESSAGE_IS_EMPTY
            )

    def _check_if_thread_id_is_missing(self, cleaned_data):
        """Check thread id when creating a new post."""

        thread_id = cleaned_data.get("thread_id")
        form_type = cleaned_data.get('form_type')
        if form_type == 'new_post' and not thread_id:
            raise ValidationError(
                _('Thread ID is not specified when creating a new post'),
                code=self.ERROR_MISSING_THREAD_ID
            )
