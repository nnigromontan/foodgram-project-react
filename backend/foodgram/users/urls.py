"""Адреса приложения users проекта foodgram."""

from django.urls import include, path

from .views import SubscribeView, SubscriptionViewSet

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view())
]
