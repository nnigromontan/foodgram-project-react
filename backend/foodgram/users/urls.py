"""Адреса приложения users проекта foodgram."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SubscribeView, SubscriptionViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
]
