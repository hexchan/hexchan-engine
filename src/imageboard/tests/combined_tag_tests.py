from django.test import TestCase

from imageboard import wakabamark


class NestedTagsTest(TestCase):
    def test_em_plus_strong(self):
        self.assertEqual(
            '<p><em>nomad</em></p>',
            wakabamark.parse_text('*nomad*'),
        )

        self.assertEqual(
            '<p>* <em>nomad</em> *</p>',
            wakabamark.parse_text('* *nomad* *'),
        )

        self.assertEqual(
            '<p><strong>nomad</strong></p>',
            wakabamark.parse_text('**nomad**'),
        )

        self.assertEqual(
            '<p>***nomad***</p>',
            wakabamark.parse_text('***nomad***'),
        )

        self.assertEqual(
            '<p>** <em>nomad</em> **</p>',
            wakabamark.parse_text('** *nomad* **'),
        )

        self.assertEqual(
            '<p>* <strong>nomad</strong> *</p>',
            wakabamark.parse_text('* **nomad** *'),
        )

        self.assertEqual(
            '<p>** <strong>nomad</strong> **</p>',
            wakabamark.parse_text('** **nomad** **'),
        )

        self.assertEqual(
            '<p>** <strong>nomad</strong> **</p>',
            wakabamark.parse_text('** __nomad__ **'),
        )

        self.assertEqual(
            '<p>__ <em>nomad</em> __</p>',
            wakabamark.parse_text('__ *nomad* __'),
        )

        self.assertEqual(
            '<p>_ <strong>nomad</strong> _</p>',
            wakabamark.parse_text('_ **nomad** _'),
        )

    def test_multi_words(self):
        self.assertEqual(
            '<p><strong>nomad**huita</strong></p>',
            wakabamark.parse_text('**nomad**huita**'),
        )

        self.assertEqual(
            '<p><strong>nomad</strong> atata <strong>huita</strong></p>',
            wakabamark.parse_text('**nomad** atata **huita**'),
        )

        self.assertEqual(
            '<p><strong>nomad</strong> atata <strong>huita</strong></p>',
            wakabamark.parse_text('__nomad__ atata **huita**'),
        )

    def test_blockquote(self):
        self.assertEqual(
            '<blockquote>&gt;&gt; some_quote</blockquote>',
            wakabamark.parse_text('&gt;&gt; some_quote'),
        )

    def test_urls_and_whitespaces(self):
        self.assertEqual(
            'Please visit <a href="http://example.com" rel="nofollow">http://example.com</a> every day.',
            wakabamark.make_url_tags('Please visit http://example.com every day.'),
        )

    def test_simple_paragraph(self):
        self.assertEqual(
            '<p>nomad<br/>atata<br/>huita</p>',
            wakabamark.parse_text('nomad\natata\nhuita'),
        )

    def test_simple_quote(self):
        self.assertEqual(
            '<blockquote>&gt;nomad<br/>&gt;atata<br/>&gt;huita</blockquote>',
            wakabamark.parse_text('&gt;nomad\n&gt;atata\n&gt;huita'),
        )

    def test_multiple_paragraphs(self):
        self.assertEqual(
            '<p>nomad</p><p>huita</p>',
            wakabamark.parse_text('nomad\n\nhuita'),
        )

    def test_combined_quote_and_paragraph_and_empty_line(self):
        self.assertEqual(
            '<p>nomad</p><blockquote>&gt;atata</blockquote><p>huita</p><p>jigurda</p>',
            wakabamark.parse_text('nomad\n&gt;atata\nhuita\n\njigurda'),
        )
