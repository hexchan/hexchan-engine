from django.urls import path, register_converter

from . import views
from . import converters


register_converter(converters.ThreadHidConverter, 'tid')
register_converter(converters.PostHidConverter, 'pid')


urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('session/', views.session_data_view, name='session'),
    path('create/', views.posting_view, name='posting_view'),
    path('<str:board_hid>/', views.board_page, name='board_page'),
    path('<str:board_hid>/<int:page_num>/', views.board_page, name='board_page_num'),
    path('<str:board_hid>/catalog/', views.catalog_page, name='catalog_page'),
    path('<str:board_hid>/<tid:thread_hid>/', views.thread_page, name='thread_page'),
    path('<str:board_hid>/<tid:thread_hid>/<pid:post_hid>/', views.post_popup, name='post_popup'),
]
