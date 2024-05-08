"""Сериализаторы для работы с рецептами."""

import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from foodgram_backend.constants import (
    MAX_COOKING_TIME,
    MAX_INGREDIENT_AMOUNT,
    MIN_COOKING_TIME,
    MIN_INGREDIENT_AMOUNT
)
from users.serializers import UserGetSerializer

from .models import (
    Ingredient,
    Recipe,
    RecipeIngridientList,
    Tag
)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор изображений."""

    def to_internal_value(self, data):
        """Преобразование изображения."""

        if isinstance(data, str) and data.startswith('data:image'):
            image_format, image_string = data.split(';base64,')
            ext = image_format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(image_string),
                name='img.' + ext,
            )

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngridientWithAmountSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента с количеством."""

    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngridientList
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэга."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецепта."""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserGetSerializer(
        read_only=True,
    )
    ingredients = IngridientWithAmountSerializer(
        read_only=True,
        many=True,
        source='ingredient_recipe',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Проверка наличия в избранном."""

        user = self.context['request'].user
        if user.is_authenticated:
            return user.is_favorited.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Проверка наличия в корзине."""

        user = self.context['request'].user
        if user.is_authenticated:
            return user.is_in_shopping_cart.filter(recipe=obj).exists()
        return False


class IngredientWithAmountCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ингридиента с привязкой колдичества."""

    id = serializers.IntegerField(
        source='ingredient.id'
    )
    amount = serializers.IntegerField(
        min_value=MIN_INGREDIENT_AMOUNT,
        max_value=MAX_INGREDIENT_AMOUNT,
    )

    class Meta:
        model = RecipeIngridientList
        fields = (
            'id',
            'amount',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ингридиента рецепта."""

    ingredients = IngredientWithAmountCreateSerializer(
        many=True,
        source='ingredient_recipe',
        required=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'author',
        )

    @staticmethod
    def validate_tags(value):
        """Проверка тэга."""

        if not value:
            raise serializers.ValidationError('Отсутствуют теги')
        if len(value) != len(set(value)):
            raise serializers.ValidationError('Теги должны быть уникальными')
        return value

    @staticmethod
    def validate_ingredients(value):
        """Проверка ингридиента."""

        if not value:
            raise serializers.ValidationError('Отсутствуют ингредиенты')
        ingredient_list = set()
        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError('Ингридиент отсутствует')
            if ingredient_id in ingredient_list:
                raise serializers.ValidationError('Такой ингридиент уже есть')
            ingredient_list.add(ingredient_id)
        return value

    @staticmethod
    def create_update_ingredients_amount(ingredient_recipe, recipe):
        """Добавление/обновление количества для ингридиента."""

        ingrediens_amount = []
        for ingredient in ingredient_recipe:
            ingredient_id = ingredient['ingredient']['id']
            ingredient_amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(id=ingredient_id)
            ingrediens_amount.append(
                RecipeIngridientList(
                    ingredient=current_ingredient,
                    recipe=recipe,
                    amount=ingredient_amount),
            )
        RecipeIngridientList.objects.bulk_create(ingrediens_amount)

    def create(self, validated_data):
        ingredient_recipe = validated_data.pop('ingredient_recipe')
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_update_ingredients_amount(
            ingredient_recipe=ingredient_recipe,
            recipe=recipe,
        )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.text = validated_data.get(
            'text',
            instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get(
            'image',
            instance.image
        )
        tags = validated_data.pop(
            'tags',
            []
        )
        if not tags:
            raise serializers.ValidationError('Добавьте минимум один тэг')

        instance.tags.set(tags)

        ingredient_recipe = validated_data.pop(
            'ingredient_recipe',
            []
        )
        if not ingredient_recipe:
            raise serializers.ValidationError(
                'Добавьте минимум один ингредиент')
        instance.ingredient_recipe.all().delete()
        self.create_update_ingredients_amount(
            ingredient_recipe=ingredient_recipe,
            recipe=instance
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для карточки рецепта."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionsSerializer(UserGetSerializer):
    """Сериализатор для подписки."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        """Получение рецептов."""

        request = self.context['request']
        limit = request.query_params.get('recipes_limit')

        if request.user.is_anonymous:
            return False
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeShortSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        """Получение количества рецептов."""

        return obj.recipes.all().count()
