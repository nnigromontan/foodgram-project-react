from django.urls import include, path
from rest_framework.routers import DefaultRouter

from foodgram_api.views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]
