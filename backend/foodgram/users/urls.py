"""Адреса приложения users проекта foodgram."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users/subscriptions',
                SubscriptionViewSet,
                basename='subscriptions')
router.register(r'users/?P<user_id>\d+)/subscribe',
                SubscriptionViewSet,
                basename='subscribe')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
