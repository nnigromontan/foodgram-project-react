"""Фильтры приложения foodgram_api."""

from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    ModelChoiceFilter,
    AllValuesMultipleFilter,
    BooleanFilter)
from rest_framework.filters import SearchFilter

from .models import Recipe
from users.models import User


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class TagFilter(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

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
