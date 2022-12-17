"""Адреса приложения foodgram_api."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from foodgram_api.views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'foodgram_api'

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]
