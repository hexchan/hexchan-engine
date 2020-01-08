from django.test import TestCase

from imageboard import wakabamark
from imageboard.models import Board, Thread, Post


class WakabaBasicTagsTest(TestCase):
    def _get_url_by_hid(self, hid: str) -> str:
        return 'http://example.com/#{0}'.format(hid)

    def _get_url_by_hid_empty(self, hid: str) -> None:
        return None

    def setUp(self) -> None:
        # Create a board
        self.board = Board.objects.create(
            hid='t',
            name='testing',
            default_max_posts_num=100,
        )

        # Create a thread
        self.thread = Thread.objects.create(
            hid=16435934,  # facade in hex
            board=self.board,
            max_posts_num=self.board.default_max_posts_num,
        )

        # Create a post
        self.main_post = Post.objects.create(
            hid=16435934,  # facade in hex
            thread=self.thread,
            is_op=True,
        )

        self.ref_post = Post.objects.create(
            hid=14613198,  # deface in hex
            thread=self.thread,
            is_op=False,
        )

        self.main_post.refs.add(self.ref_post)

    def test_basic_em(self):
        self.assertEqual(
            '<em>nomad</em>',
            wakabamark.make_em_tags('*nomad*'),
        )

        self.assertEqual(
            '<em>nomad</em>',
            wakabamark.make_em_tags('_nomad_'),
        )

    def test_basic_strong(self):
        self.assertEqual(
            '<strong>nomad</strong>',
            wakabamark.make_strong_tags('**nomad**'),
        )

        self.assertEqual(
            '<strong>nomad</strong>',
            wakabamark.make_strong_tags('__nomad__'),
        )

    def test_basic_strike(self):
        self.assertEqual(
            '<s>nomad</s>',
            wakabamark.make_strike_tags('--nomad--'),
        )

    def test_basic_spoiler(self):
        self.assertEqual(
            '<span class="spoiler">nomad</span>',
            wakabamark.make_spoiler_tags('%%nomad%%'),
        )

    def test_basic_ref(self):
        self.assertEqual(
            '<a class="ref js-ref" href="/t/0xfacade/#0xdeface">&gt;&gt;0xdeface</a>',
            wakabamark.make_ref_tags('&gt;&gt;0xdeface', self.main_post)
        )

        self.assertEqual(
            '<span class="dead_ref">&gt;&gt;0xdabbed</span>',
            wakabamark.make_ref_tags('&gt;&gt;0xdabbed', self.main_post)
        )

    def test_basic_urls(self):
        self.assertEqual(
            'Please visit <a href="http://example.com" rel="nofollow">http://example.com</a>',
            wakabamark.make_url_tags('Please visit http://example.com'),
        )
