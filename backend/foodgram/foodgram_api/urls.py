"""Адреса приложения foodgram_api."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from foodgram_api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import SubscriptionViewSet

app_name = 'foodgram_api'

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
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
]
