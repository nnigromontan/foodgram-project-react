"""Адреса приложения users проекта foodgram."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscribeView, SubscriptionViewSet, CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'users/subscriptions',
                SubscriptionViewSet,
                basename='subscriptions')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/',
         SubscribeView.as_view(),
         name='subscribe')
]
