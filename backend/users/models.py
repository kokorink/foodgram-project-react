"""Описание модели пользователя сервиса."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from foodgram_backend.constants import (USER_EMAIL_MAX_LENGTH,
                                        USER_NAMES_PASSWORD_MAX_LENGTH)

ADMIN = 'admin'
USER = 'user'

ROLE_CHOICES = (
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
)


class User(AbstractUser):
    """Модель пользователя."""

    username_regex = RegexValidator(regex=r'^[\w.@+-]+\Z', message='Некорректное имя пользоватея')
    username = models.CharField(validators=(username_regex,), verbose_name='Логин пользователя',
                                max_length=USER_NAMES_PASSWORD_MAX_LENGTH, unique=True, blank=False, null=False)
    email = models.EmailField('Эл.почта', max_length=USER_EMAIL_MAX_LENGTH, unique=True)
    role = models.CharField('Роль', default=USER, max_length=USER_NAMES_PASSWORD_MAX_LENGTH, choices=ROLE_CHOICES)
    first_name = models.CharField('Имя', max_length=USER_NAMES_PASSWORD_MAX_LENGTH, blank=False, null=False)
    last_name = models.CharField('Фамилия', max_length=USER_NAMES_PASSWORD_MAX_LENGTH, blank=False)
    password = models.CharField("Пароль", null=False, max_length=USER_NAMES_PASSWORD_MAX_LENGTH)
    is_active = models.BooleanField("Активен", default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (models.UniqueConstraint(fields=('email', 'username'), name='unique_user'),)

    def str(self):
        return self.username


class Subscription(models.Model):
    """Модель для подписок."""

    user = models.ForeignKey(User, related_name='subscriber', verbose_name="Подписчик", on_delete=models.CASCADE,)
    author = models.ForeignKey(User, related_name='subscribe_author', verbose_name="Автор", on_delete=models.CASCADE,)

    def clean(self):
        """Проверка на самоподписку."""

        if self.user == self.author:
            raise ValidationError("Нельзя подписаться на самого себя")

    def save(self, *args, **kwargs):
        """Переопределение сохранения с учётом проверки."""

        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = (models.UniqueConstraint(fields=('user', 'author'), name='unique_subscription'),)
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def str(self):
        return f'{self.user} подписан на {self.author}'
