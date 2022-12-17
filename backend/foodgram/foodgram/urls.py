"""Адреса проекта foodgram."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'^api/', include('users.urls', namespace='users')),
    path(r'^api/', include('foodgram_api.urls', namespace='foodgram_api')),
    path(r'^api/', include('djoser.urls')),
    path(r'^api/auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns = (
        urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
