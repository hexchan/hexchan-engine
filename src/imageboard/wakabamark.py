"""Regular expressions ported from Wakaba.

See wakabautils.pl file in Wakaba package.
Version 3.0.9 was used.

Synthax: http://wakaba.c3.cx/docs/docs.html#WakabaMark

TODO: document regular expressions
TODO: tests
TODO: move ref expression to app config

Missing features:
TODO: code
TODO: lists
"""

import re

from hexchan import config


def make_url_tags(line: str) -> str:
    """Find URLs in string and replace them with <a> tags."""
    return re.sub(
        r"""
            (
                (?:http://|https://|ftp://|mailto:|news:|irc:)
                [^\s<>()"]*?
                (?:\([^\s<>()"]*?\)[^\s<>()"]*?)*
            )
            (
                (?:\s|<|>|"|\.||\]|!|\?|,|&\#44;|&quot;)*
                (?:[\s<>()"]|$)
            )
        """,
        r'<a href="\1" rel="nofollow">\1</a>\2',
        line,
        flags=re.X
    )


def make_em_tags(line: str) -> str:
    """Find emphasis marks in string and replace them with <em> tags."""
    return re.sub(
        r"""
            (?<![\w*])
            (\*|_)
            (?![<>\s*_])
            ([^<>]+?)
            (?<![<>\s*_])
            \1 (?![\w*])
        """,
        r'<em>\2</em>',
        line,
        flags=re.X
    )


def make_strong_tags(line: str) -> str:
    """Find strong marks in string and replace them with <strong> tags."""
    return re.sub(
        r"""
            (?<![\w*_])
            (\*\*|__)
            (?![<>\s\*_])
            ([^<>]+?)
            (?<![<>\s*_])
            \1
            (?![\w*_])
        """,
        r'<strong>\2</strong>',
        line,
        flags=re.X
    )


def make_spoiler_tags(line: str) -> str:
    """Find spoiler marks in string and replace them with <span class="spoiler"> tags."""
    return re.sub(
        r"""
            (?<![\w%])
            (%%)
            (?![<>\s%])
            ([^<>]+?)
            (?<![<>\s%])
            \1
            (?![\w%])
        """,
        r'<span class="spoiler">\2</span>',
        line,
        flags=re.X
    )


def make_strike_tags(line: str) -> str:
    """Find strike marks in string and replace them with <s> tags."""
    return re.sub(
        r"""
            (?<![\w-])
            (--)
            (?![<>\s-])
            ([^<>]+?)
            (?<![<>\s-])
            \1
            (?![\w-])
        """,
        r'<s>\2</s>',
        line,
        flags=re.X
    )


def make_ref_tags(line: str, post=None) -> str:
    """Find post refs and replace them with links to those posts."""

    search_expression = re.compile(
        r'&gt;&gt;({})'.format(config.POST_HID_REGEX)
    )

    def replacement_function(matchobj):
        hid = matchobj.group(1)
        hid_int = int(hid, 16)
        url = post.ref_urls.get(hid_int) if post is not None else None

        if url is not None:
            return '<a class="ref js-ref" href="{url}">&gt;&gt;{hid}</a>'.format(url=url, hid=hid)
        else:
            return '<span class="dead_ref">&gt;&gt;{hid}</span>'.format(hid=hid)

    return search_expression.sub(replacement_function, line)


def parse_text(text: str, post=None, make_refs=True, make_links=True) -> str:
    """Make all text blocks with inline tags."""

    full_text = ''

    # TODO: lists and code
    non_paragraph_block_regex = r'^(?:\s*$|&gt;)'  # empty lines and quotes
    empty_line_regex = r'^\s*$'
    quote_line_regex = r'^&gt;'
    newline_regex = r'(?:\r\n|\n|\r)'

    # Split text line by line
    text_lines = re.split(newline_regex, text)
    if len(text_lines) == 0:
        return ''

    while len(text_lines) > 0:
        line = text_lines[0]

        # Skip empty lines
        if re.match(empty_line_regex, line):
            del text_lines[0]

        # Detect start of quote block (aka "greentext")
        elif re.match(quote_line_regex, line):
            full_text += '<blockquote>'
            quote_lines = []
            while len(text_lines) > 0:
                quote_line = text_lines[0]
                if re.match(quote_line_regex, quote_line):
                    quote_lines.append(
                        format_line(quote_line, post, make_refs, make_links)
                    )
                    del text_lines[0]
                else:
                    break
            full_text += '<br/>'.join(quote_lines) + '</blockquote>'

        else:
            full_text += '<p>'
            p_lines = []
            while len(text_lines) > 0:
                p_line = text_lines[0]
                if not re.match(non_paragraph_block_regex, p_line):
                    p_lines.append(
                        format_line(p_line, post, make_refs, make_links)
                    )
                    del text_lines[0]
                else:
                    break
            full_text += '<br/>'.join(p_lines) + '</p>'

    return full_text


def format_line(line: str, post=None, make_refs=True, make_links=True) -> str:
    formatted_line = line
    if make_links:
        formatted_line = make_url_tags(formatted_line)
    formatted_line = make_strong_tags(formatted_line)
    formatted_line = make_em_tags(formatted_line)
    formatted_line = make_strike_tags(formatted_line)
    formatted_line = make_spoiler_tags(formatted_line)
    if make_refs:
        formatted_line = make_ref_tags(formatted_line, post)

    return formatted_line


def extract_refs(text: str) -> list:
    """Extract post refs from text."""

    search_expression = re.compile(
        r'&gt;&gt;({})'.format(config.POST_HID_REGEX)
    )

    hex_hids = search_expression.findall(text)

    int_hids = [int(hid, 16) for hid in hex_hids]

    return int_hids
