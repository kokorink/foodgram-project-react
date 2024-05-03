from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
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
        return self.name


class Ingredient(models.Model):
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
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=False)
    name = models.CharField('Рецепт', max_length=200, null=False)
    image = models.ImageField('Изображение', upload_to='collected_static/images/', null=False, default=None)
    text = models.TextField('Описание', null=False)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipe', verbose_name='Ингридиенты', null=False)
    tags = models.ManyToManyField(Tag, related_name='recipe', verbose_name='Тэги', null=False)
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
        return self.name


class RecipeTag(models.Model):
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
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингридиент рецепта")
    amount = models.IntegerField('Количество',
                                 validators=[MinValueValidator(1, message='Минимум 1!')])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_list', verbose_name="Рецепт")

    class Meta:
        verbose_name = 'ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'amount', 'recipe'),
                name='unique_ingredient_recipe'
            )]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}{self.ingredient.measurement_unit}'
