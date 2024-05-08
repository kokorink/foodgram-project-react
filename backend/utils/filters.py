"""Описание фильтров для приложения recipes."""
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    """Фильтры модели Ingredient."""

    search_param = 'name'
