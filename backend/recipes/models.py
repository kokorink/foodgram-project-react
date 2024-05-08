"""Описание моделей для рецепта"""

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField('Тэг', max_length=200, unique=True, null=False)
    color = models.CharField('Цвет', max_length=7, unique=True, null=False)
    slug = models.SlugField('Слаг', max_length=200, unique=True, null=False)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='unique_tag'
            )]

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField('Ингридиент', max_length=200, null=False)
    measurement_unit = models.TextField('Единица измерения', null=False)

    class Meta:
        verbose_name = 'ингридинет'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )]

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=False,
                               related_name="recipes",)
    name = models.CharField('Рецепт', max_length=200, null=False)
    image = models.ImageField('Изображение', upload_to='images/', null=False, default=None)
    text = models.TextField('Описание', null=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngridientList', related_name='recipe',
                                         verbose_name='Ингридиенты')
    tags = models.ManyToManyField(Tag, related_name='recipe', verbose_name='Тэги')
    cooking_time = models.IntegerField('Время приготовления в минутах', null=False)
    pub_date = models.DateTimeField('Дата и время публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name', 'text'),
                name='unique_recipe'
            )]

    def __str__(self):
        return str(self.name)


class RecipeTag(models.Model):
    """Модель связки теэгов и рецепта."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тэг рецепта")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт тэга")

    class Meta:
        verbose_name = 'тэг-рецепт'
        verbose_name_plural = 'Тэг-рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='unique_tag_recipe'
            )]

    def __str__(self):
        return f'{self.tag} - {self.recipe}'


class RecipeIngridientList(models.Model):
    """Модель связки ингридиентов с их количеством и рецептом."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингридиент рецепта",
                                   related_name="ingredient_in_recipes")
    amount = models.IntegerField('Количество',
                                 validators=[MinValueValidator(1, message='Минимум 1!')])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")

    class Meta:
        default_related_name = 'ingredient_recipe'
        verbose_name = 'ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'amount', 'recipe'),
                name='unique_ingredient_recipe'
            )]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}{self.ingredient.measurement_unit}'


class Favorite(models.Model):
    """Модель для добавления рецепта в избранное."""

    user = models.ForeignKey(User, related_name='is_favorited', on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'в избранном'
        verbose_name_plural = 'В избранных'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited_user_recipe'
            ),
        )


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(User, related_name='is_in_shopping_cart', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    class Meta:
        verbose_name = 'в корзине'
        verbose_name_plural = 'В корзине'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart_user_recipe'
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.recipe}'
