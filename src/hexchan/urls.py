from django.urls import path, include
from django.contrib import admin
from django.conf import settings


urlpatterns = []

if settings.DEBUG:
    # Django debug toolbar
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    # Static files
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('imageboard.urls')),
]
