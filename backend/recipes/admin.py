from django.contrib import admin

from .models import Recipe, Ingredient, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Представление модели User."""

    list_display = ('id',
                    'author',
                    'name',
                    'text',
                    # 'ingredients',
                    # 'tags',
                    'cooking_time',
                    'pub_date'
                    )
    list_editable = ('author', 'cooking_time')
    search_fields = ('author', 'name',)
    list_display_links = ('name',)
    ordering = ('-pub_date',)


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit')
    ordering = 'name',
    search_fields = ('name', 'author')
    list_display_links = ('name',)


class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'color', 'slug')
    ordering = 'name',
    search_fields = ('name',)
    list_display_links = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)