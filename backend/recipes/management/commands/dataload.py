"""Команда для наполнения БД данными об ингридиентах и тэгах."""
from django.core.management.base import BaseCommand
from rest_framework.utils import json

from foodgram_backend.settings import BASE_DIR
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    """Класс команды."""
    help = ('Команда для наполнения БД данными об ингридиентах и тэгах. При этом ингридиенты загружаются из фикстуры '
            'data/ingredients.json, располагающейся в корне проекта. Формат принимаемых данных: '
            '{"ingridients": [{"name": "data_name", "measurement_unit": "data_measurement_unit"}, ]}')

    def handle(self, *args, **options):
        """Вызов собственных методов класса."""

        self.load_ingredients()
        self.create_tags()
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))

    @staticmethod
    def load_ingredients():
        """Загрузка ингридиентов из ingredients.json."""

        if not Ingredient.objects.all().exists():
            path = BASE_DIR.joinpath('data', 'ingredients.json')
            with open(path, 'r', encoding='utf8') as file:
                data = json.load(file)
                ingredients = []
                for ingredient in data['ingridients']:
                    ingredients.append(Ingredient(
                        name=ingredient['name'],
                        measurement_unit=ingredient['measurement_unit']
                    ))
                Ingredient.objects.bulk_create(ingredients)

    @staticmethod
    def create_tags():
        """Добавление тэгов."""

        if not Tag.objects.all().exists():
            breakfast_tag = Tag(name='Завтрак',
                                color='#000000',
                                slug='breakfast')
            brunch_tag = Tag(name='Бранч',
                             color='#FF0000',
                             slug='brunch')
            lunch_tag = Tag(name='Обед',
                            color='#00FF00',
                            slug='lunch')
            dinner_tag = Tag(name='Ужин',
                             color='#0000FF',
                             slug='dinner')
            Tag.objects.bulk_create([breakfast_tag,
                                     brunch_tag,
                                     lunch_tag,
                                     dinner_tag])
