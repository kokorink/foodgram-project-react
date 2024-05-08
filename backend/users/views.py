"""Вьюсет для пользователей."""

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.serializers import SubscriptionsSerializer

from .models import Subscription, User


class UserViewSet(UserViewSet):
    """Переопределние вьюсета для пользователя."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        """Получение своих данных."""

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def subscriptions(self, request):
        """Получение данных о подписках."""

        subscribers = User.objects.filter(email=request.user)
        page = self.paginate_queryset(subscribers)
        serializer = SubscriptionsSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        """Добавление и удаление подписки."""

        user = request.user
        subscriber = get_object_or_404(User, pk=id)
        subscription = user.subscribe_author.filter(user=subscriber)

        if request.method == 'POST' and user != subscriber and not subscription.exists():
            Subscription.objects.create(author=user, user=subscriber)
            serializer = SubscriptionsSerializer(subscriber,
                                                 context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE' and subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
