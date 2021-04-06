from django.urls import path, register_converter

from . import views
from . import converters


register_converter(converters.ThreadHidConverter, 'tid')
register_converter(converters.PostHidConverter, 'pid')


urlpatterns = [
    path(
        '',
        views.StartPage.as_view(),
        name='start_page'
    ),
    path(
        'session/',
        views.session_data_view,
        name='session'
    ),
    path(
        'create/',
        views.PostingView.as_view(),
        name='posting_view'
    ),
    path(
        'captcha/',
        views.captcha_view,
        name='captcha_view'
    ),
    path(
        '<str:board_hid>/',
        views.BoardPage.as_view(),
        name='board_page'
    ),
    path(
        '<str:board_hid>/<int:page_num>/',
        views.BoardPage.as_view(),
        name='board_page_num'
    ),
    path(
        '<str:board_hid>/catalog/',
        views.CatalogPage.as_view(),
        name='catalog_page'
    ),
    path(
        '<str:board_hid>/<tid:thread_hid>/',
        views.ThreadPage.as_view(),
        name='thread_page'
    ),
    path(
        '<str:board_hid>/<tid:thread_hid>/<pid:post_hid>/',
        views.PostPage.as_view(),
        name='post_popup'
    ),
]
