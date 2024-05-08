"""Описание админ-зоны для моделей приложения recipes."""
from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    RecipeIngridientList,
    Tag,
)


class RecipeAdmin(admin.ModelAdmin):
    """Представление модели рецепта."""

    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',
        'pub_date',
    )
    list_editable = (
        'author',
        'cooking_time',
    )
    search_fields = (
        'author',
        'name',
    )
    list_display_links = (
        'name',
    )
    ordering = (
        '-pub_date',
    )


class IngredientAdmin(admin.ModelAdmin):
    """Представление модели ингридиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )
    ordering = (
        'name',
    )
    search_fields = (
        'name',
        'author',
    )
    list_display_links = (
        'name',
    )


class TagAdmin(admin.ModelAdmin):
    """Представление модели тэгов."""

    list_display = (
        'name',
        'color',
        'slug',
    )
    ordering = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_display_links = (
        'name',
    )


class RecipeIngridientListAdmin(admin.ModelAdmin):
    """Представление связки моделей рецептов и ингридиентов."""

    list_display = (
        'ingredient',
        'amount',
        'recipe',
    )
    list_display_links = (
        'ingredient',
    )
    ordering = (
        'recipe',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngridientList, RecipeIngridientListAdmin)
