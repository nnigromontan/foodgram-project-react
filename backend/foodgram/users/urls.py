"""Адреса приложения users проекта foodgram."""

from django.urls import include, path

from users.views import SubscribeView, CreateUserView

urlpatterns = [
    path('subscriptions/', CreateUserView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('<int:pk>/subscribe/', SubscribeView.as_view())
]
