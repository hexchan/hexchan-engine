# Django imports
from django.test import TestCase
from django.test import Client

# App imports
from imageboard.models import Board, Thread, Post
from captcha.models import Captcha


class NewThreadTestCase(TestCase):
    def setUp(self):
        # Init testing client
        self.client = Client()

        # Create a board
        self.board = Board.objects.create(
            hid='t',
            name='testing',
            default_max_posts_num=100,
        )

        # Create a captcha
        Captcha.objects.create(
            public_id='100500',
            solution='swordfish',
            image='null',
        )

        # Update session with captcha info with this request
        self.client.get('/captcha/')

        # Base post content dict
        self.base_post_content = {
            'form_type': 'new_thread',
            'board_id': self.board.id,
            'captcha_0': 'swordfish',
            'captcha_1': '100500',
            'title': 'Test title',
            'author': 'Tester',
            'email': '',
            'text': 'Test test test test',
            'password': 'swordfish',
        }

    def check_redirect(self, response):
        # Check for handled exceptions
        if response.status_code != 302:
            e = response.context.get('exception')
            self.assertEqual(e, None)

        # Check for correct redirect
        self.assertRedirects(response, '/t/0x000000/', status_code=302, target_status_code=200)

    def test_create_thread(self):
        post_data = self.base_post_content.copy()
        post_data.update({})
        response = self.client.post('/create/', post_data)

        self.check_redirect(response)

    def test_thread_flushing(self):
        # TODO
        pass
