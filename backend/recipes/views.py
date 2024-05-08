"""Описание вьюлсетов для приложения рецептов."""

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet
)

from utils.filters import IngredientFilter
from utils.pagination import PageNumberPagination
from utils.permissinos import IsAuthorOrReadOnly
from utils.renders import ShoppingCartToTXTExport

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngridientList,
    ShoppingCart,
    Tag,
)
from .serializers import (
    IngredientSerializer,
    IngridientWithAmountSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    RecipeShortSerializer,
    TagSerializer,
)


class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """Вьюсет для ингридиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (
        AllowAny,
    )
    filter_backends = (
        IngredientFilter,
    )
    search_fields = (
        '^name',
    )
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тэга."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецепта."""

    permission_classes = (
        IsAuthorOrReadOnly,
    )
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = (
        'author',
    )

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()
        query_params = self.request.query_params
        tags = query_params.getlist('tags')
        is_favorited = query_params.get('is_favorited')
        is_in_shopping_cart = query_params.get('is_in_shopping_cart')

        if tags and is_favorited and user.is_authenticated:
            return queryset.filter(
                tags__slug__in=tags,
                favorited__user=user
            ).distinct()
        if tags:
            return queryset.filter(
                tags__slug__in=tags
            ).distinct()
        if is_in_shopping_cart and user.is_authenticated:
            return queryset.filter(
                shoppingcart__user=user
            )
        if is_favorited and user.is_authenticated:
            return queryset.filter(
                favorite__user=user
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk):
        """Добавление/удаление рецепта в избранное."""

        try:
            recipe = Recipe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            if request.method == 'POST':
                return Response(status=HTTP_400_BAD_REQUEST)
            return Response(status=HTTP_404_NOT_FOUND)
        user = request.user
        favorite_recipe = user.is_favorited.filter(recipe=recipe)

        if request.method == 'POST' and not favorite_recipe.exists():
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE' and favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Добавление/удаление ингридиентов рецепта в спиисок покупок."""

        try:
            recipe = Recipe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            if request.method == 'POST':
                return Response(status=HTTP_400_BAD_REQUEST)
            return Response(status=HTTP_404_NOT_FOUND)
        user = request.user
        favorite_recipe = user.is_in_shopping_cart.filter(recipe=recipe)

        if request.method == 'POST' and not favorite_recipe.exists():
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE' and favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            renderer_classes=(ShoppingCartToTXTExport,)
            )
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""

        user = request.user
        ingredient = RecipeIngridientList.objects.filter(
            recipe__shoppingcart__user=user)
        if ingredient:
            now = timezone.now()
            file_name = (
                f'Shopping_list_{now:%Y-%m-%d_%H-%M-%S}'
                f'.{request.accepted_renderer.format}'
            )
            serializer = IngridientWithAmountSerializer(
                ingredient,
                many=True
            )
            return Response(
                serializer.data,
                headers={
                    'Content-Disposition':
                    f"attachment; filename='{file_name}'"
                }
            )
        return Response(status=HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer
