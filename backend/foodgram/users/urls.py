"""Адреса приложения users проекта foodgram."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscribeView, SubscriptionViewSet, CustomUserViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/',
         SubscriptionViewSet.as_view(),
         name='subscribtions'),
    path('users/<int:pk>/subscribe/',
         SubscribeView.as_view(),
         name='subscribe')
]
