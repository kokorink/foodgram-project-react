from django.db import models
from users.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField('Тэг', max_length=200, unique=True, null=False)
    color = models.CharField('Цвет', max_length=7, unique=True, null=False)
    slug = models.SlugField('Слаг', max_length=200, unique=True, null=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Ингридиент', max_length=200, null=False)
    measurement_unit = models.TextField('', null=False)
    amount = models.IntegerField('Количество', null=False)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=False)
    name = models.CharField('Рецепт', max_length=200, null=False)
    image = models.ImageField('Изображение', upload_to='collected_static/images/', null=False, default=None)
    text = models.TextField('Описание', null=False)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipe', verbose_name='Ингридиенты', null=False)
    tags = models.ManyToManyField(Tag, related_name='recipe', verbose_name='Тэги', null=False)
    cooking_time = models.IntegerField('Время приготовления в минутах', null=False)

    def __str__(self):
        return self.name
