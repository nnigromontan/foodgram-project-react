"""Адреса приложения users проекта foodgram."""

from django.urls import include, path

from users.views import SubscribeView, SubscriptionViewSet

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
]
