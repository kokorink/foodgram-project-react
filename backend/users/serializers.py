from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(UserCreateSerializer):
    """Переопределение серриализатора для создания пользователя."""

    def validate(self, attrs):
        return attrs


class UserGetSerializer(serializers.ModelSerializer):
    """Серриализатор для получения данных о пользователе."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Получение данных о наличии подписок."""

        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return obj.subscriber.filter(user=request.user).exists()
