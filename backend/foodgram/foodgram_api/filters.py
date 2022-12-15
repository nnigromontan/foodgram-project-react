"""Фильтры приложения foodgram_api."""
from django_filters import rest_framework as filters

from .models import Recipe, Ingredient
from users.models import User


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",
                              lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
            return queryset.filter(users_favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
