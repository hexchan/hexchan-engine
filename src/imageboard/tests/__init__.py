from .basic_tag_tests import WakabaBasicTagsTest
from .combined_tag_tests import NestedTagsTest

from .test_new_post import NewPostTestCase
from .test_new_thread import NewThreadTestCase
from .test_posting_exceptions import PostingExceptionsTestCase


__all__ = [
    'WakabaBasicTagsTest',
    'NestedTagsTest',
    'NewPostTestCase',
    'NewThreadTestCase',
    'PostingExceptionsTestCase',
]
