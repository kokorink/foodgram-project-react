from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram_backend.constants import (INGREDIENT_NAME_UNIT_MAX_LENGTH,
                                        MAX_COOKING_TIME,
                                        MAX_INGREDIENT_AMOUNT,
                                        MIN_COOKING_TIME,
                                        MIN_INGREDIENT_AMOUNT,
                                        RECIPE_NAME_MAX_LENGTH,
                                        TAG_COLOR_MAX_LENGTH,
                                        TAG_NAME_SLUG_MAX_LENGTH)

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Тэг',
        max_length=TAG_NAME_SLUG_MAX_LENGTH,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=TAG_COLOR_MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=TAG_NAME_SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='unique_tag'),
        )

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        'Ингридиент',
        max_length=INGREDIENT_NAME_UNIT_MAX_LENGTH,
    )
    measurement_unit = models.TextField(
        'Единица измерения',
        max_length=INGREDIENT_NAME_UNIT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'ингридинет'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'),
        )

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    name = models.CharField(
        'Рецепт',
        max_length=RECIPE_NAME_MAX_LENGTH,
        null=False
    )
    image = models.ImageField(
        'Изображение',
        upload_to='images/',
        default=None,
    )
    text = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngridientList',
        related_name='recipe',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Тэги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message='Минимум 1 минута!'),
            MaxValueValidator(
                MAX_COOKING_TIME,
                message='Максимум 32000!'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name', 'text'),
                name='unique_recipe'),
        )
        ordering = ("-pub_date",)

    def __str__(self):
        return str(self.name)


class RecipeTag(models.Model):
    """Модель связки теэгов и рецепта."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэг рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт тэга'
    )

    class Meta:
        verbose_name = 'тэг-рецепт'
        verbose_name_plural = 'Тэг-рецепты'
        constraints = (models.UniqueConstraint(
            fields=('tag', 'recipe'),
            name='unique_tag_recipe'),
        )

    def __str__(self):
        return f'{self.tag} - {self.recipe}'


class RecipeIngridientList(models.Model):
    """Модель связки ингридиентов с их количеством и рецептом."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент рецепта',
        related_name='ingredient_in_recipes'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_INGREDIENT_AMOUNT,
                message='Минимум 1!'
            ),
            MaxValueValidator(
                MAX_INGREDIENT_AMOUNT,
                message='Максимум 32000!'
            )
        ]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = 'ingredient_recipe'
        verbose_name = 'ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'amount', 'recipe'),
                name='unique_ingredient_recipe'),
        )

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f'{self.ingredient.measurement_unit}')


class Favorite(models.Model):
    """Модель для добавления рецепта в избранное."""

    user = models.ForeignKey(
        User, related_name='is_favorited',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'в избранном'
        verbose_name_plural = 'В избранных'
        ordering = ('user',)
        constraints = (models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='unique_favorited_user_recipe'),
        )


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        related_name='is_in_shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'в корзине'
        verbose_name_plural = 'В корзине'
        ordering = ('user',)
        constraints = (models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='unique_shopping_cart_user_recipe'),
        )

    def __str__(self):
        return f'{self.user} - {self.recipe}'
