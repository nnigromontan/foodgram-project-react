"""Адреса приложения users проекта foodgram."""

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import SubscriptionViewSet

app_name = 'users'

router = SimpleRouter()
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscriptionViewSet,
    basename='subscribe')
router.register(
    r'users/subscriptions/',
    SubscriptionViewSet,
    basename='subscriptions')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
