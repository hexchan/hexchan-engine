# Standard imports
import os.path
import datetime

# Django imports
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import NON_FIELD_ERRORS

# App imports
from imageboard.models import Board, Thread
from imageboard.forms import PostingForm

from imageboard.models.captcha import Captcha

from moderation.models import Ban, BanReason, ImageFilter, WordFilter


class PostingExceptionsTestCase(TestCase):
    def setUp(self):
        # Init testing client
        self.client = Client()

        # Create a board
        self.board = Board.objects.create(
            hid='t',
            name='testing',
            default_max_posts_num=100,
        )

        # Create a thread
        self.thread = Thread.objects.create(
            hid=0,
            board=self.board,
            max_posts_num=self.board.default_max_posts_num,
        )

        # Create a captcha
        Captcha.objects.create(
            solution='swordfish',
            thread=self.thread,
            board=self.board,
            ip_address='127.0.0.1',
        )

        # Base post content dict
        self.base_post_content = {
            'form_type': 'new_post',
            'board_id': self.board.id,
            'thread_id': self.thread.id,
            'captcha': 'swordfish',
            'title': 'Test title',
            'author': 'Tester',
            'email': '',
            'text': 'Test test test test',
            'password': 'swordfish',
        }

        # Prepare upload dirs
        (settings.STORAGE_DIR / 'test').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'images').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'thumbs').mkdir(parents=True, exist_ok=True)

    def make_bad_form_request(self, post_content_mixin, field=NON_FIELD_ERRORS, error_code=None, **extra_client_kwargs):
        post_data = self.base_post_content.copy()
        post_data.update(post_content_mixin)
        response = self.client.post('/create/', post_data, **extra_client_kwargs)

        # Error template will be used with 403 status code
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'imageboard/posting_error_page.html')

        form = response.context['form']

        error_code_found = form.has_error(field, code=error_code)

        self.assertTrue(
            error_code_found,
            msg='Field {field} does not have error with code {error_code}'.format(field=field, error_code=error_code)
        )

    def test_form_validation(self):
        self.make_bad_form_request({'form_type': 'bad'}, 'form_type', PostingForm.ERROR_BAD_FORM_TYPE)
        self.make_bad_form_request({'board_id': 'bad'}, 'board_id', 'invalid')
        self.make_bad_form_request({'thread_id': 'bad'}, 'thread_id', 'invalid')

    def test_board_not_found(self):
        self.make_bad_form_request(
            {'board_id': '100500'},
            'board_id',
            PostingForm.ERROR_BOARD_NOT_FOUND
        )

    def test_thread_not_found(self):
        self.make_bad_form_request(
            {'thread_id': '100500'},
            'thread_id',
            PostingForm.ERROR_THREAD_NOT_FOUND
        )

    def test_board_is_locked(self):
        locked_board = Board.objects.create(
            hid='b',
            name='random',
            default_max_posts_num=100,
            is_locked=True,
        )
        locked_thread = Thread.objects.create(
            hid=1,
            board=self.board,
            max_posts_num=1,
            is_locked=True,
        )
        self.make_bad_form_request(
            {
                'board_id': locked_board.id,
                'thread_id': locked_thread.id,
            },
            'board_id',
            PostingForm.ERROR_BOARD_IS_LOCKED
        )

    def test_thread_is_locked(self):
        locked_thread = Thread.objects.create(
            hid=1,
            board=self.board,
            max_posts_num=1,
            is_locked=True,
        )
        self.make_bad_form_request({'thread_id': locked_thread.id}, 'thread_id', PostingForm.ERROR_THREAD_IS_LOCKED)

    def test_attached_non_image(self):
        filename = os.path.join(os.path.dirname(__file__), 'not_image.txt')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_form_request(
                    {'images': fp},
                    'images',
                    PostingForm.ERROR_BAD_FILE_TYPE
                )

    def test_attached_large_image(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise_big.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_form_request({'images': fp}, 'images', PostingForm.ERROR_FILE_IS_TOO_LARGE)

    def test_attached_too_many_images(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp1, open(filename, 'rb') as fp2, open(filename, 'rb') as fp3, open(filename, 'rb') as fp4, open(filename, 'rb') as fp5, open(filename, 'rb') as fp6, open(filename, 'rb') as fp7, open(filename, 'rb') as fp8:
                self.make_bad_form_request(
                    {'images': [fp1, fp2, fp3, fp4, fp5, fp6, fp7, fp8]},
                    'images',
                    PostingForm.ERROR_TOO_MANY_FILES
                )

    def test_wordfilter(self):
        WordFilter.objects.create(expression='nomad')
        WordFilter.objects.create(expression='huita')
        self.make_bad_form_request({'text': 'nomad huita'}, 'text', PostingForm.ERROR_BAD_MESSAGE)

    def test_advanced_wordfilter(self):
        WordFilter.objects.create(expression='^huit(a|ariy)')
        WordFilter.objects.create(expression='^nomad')
        self.make_bad_form_request({'text': 'huitariy'}, 'text', PostingForm.ERROR_BAD_MESSAGE)
        self.make_bad_form_request({'text': 'nomadia'}, 'text', PostingForm.ERROR_BAD_MESSAGE)

    def test_imagefilter(self):
        # Use noise.png
        ImageFilter.objects.create(checksum='023943b7771ab11604a64ca306cc0ec4', size='82633')

        filename = os.path.join(os.path.dirname(__file__), 'noise.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_form_request({'images': fp}, 'images', PostingForm.ERROR_BAD_IMAGE)

    def test_ban_ip(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_ip = '93.184.216.34'

        Captcha.objects.create(
            solution='swordfish',
            thread=self.thread,
            board=self.board,
            ip_address=banned_ip,
        )

        Ban.objects.create(type=Ban.BAN_TYPE_IP, value=banned_ip, reason=reason, active_until=tomorrow)

        self.make_bad_form_request({}, NON_FIELD_ERRORS, PostingForm.ERROR_BANNED, REMOTE_ADDR=banned_ip)

    def test_ban_session(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_session = self.client.session.session_key

        Ban.objects.create(type=Ban.BAN_TYPE_SESSION, value=banned_session, reason=reason, active_until=tomorrow)

        self.make_bad_form_request({}, NON_FIELD_ERRORS, PostingForm.ERROR_BANNED)

    def test_ban_network(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_network = '93.184.216.0/24'
        banned_ip = '93.184.216.34'

        Captcha.objects.create(
            solution='swordfish',
            thread=self.thread,
            board=self.board,
            ip_address=banned_ip,
        )

        Ban.objects.create(type=Ban.BAN_TYPE_NET, value=banned_network, reason=reason, active_until=tomorrow)

        self.make_bad_form_request({}, NON_FIELD_ERRORS, PostingForm.ERROR_BANNED, REMOTE_ADDR=banned_ip)

    def test_rapid_posting(self):
        post_data = self.base_post_content.copy()
        self.client.post('/create/', post_data)
        Captcha.objects.create(
            solution='swordfish',
            thread=self.thread,
            board=self.board,
            ip_address='127.0.0.1',
        )
        self.make_bad_form_request({}, NON_FIELD_ERRORS, PostingForm.ERROR_NOT_SO_FAST)

    def test_empty_post(self):
        self.make_bad_form_request({'text': '', 'images': []}, NON_FIELD_ERRORS, PostingForm.ERROR_MESSAGE_IS_EMPTY)
