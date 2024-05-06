"""Описание модели пользователя сервиса."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_slug, RegexValidator
from django.db import models
from rest_framework.exceptions import ValidationError

ADMIN = 'admin'
USER = 'user'

ROLE_CHOICES = (
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
)


class User(AbstractUser):
    """Модель пользователя."""

    username_regex = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Некорректное имя пользоватея'
    )
    username = models.CharField(
        validators=(username_regex,),
        verbose_name='Логин пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField('Эл.почта', max_length=settings.EMAIL_MAX_LENGTH, unique=True)
    role = models.CharField('Роль', default=USER, max_length=settings.USERNAME_MAX_LENGTH, choices=ROLE_CHOICES)
    first_name = models.CharField('Имя', max_length=settings.USERNAME_MAX_LENGTH, blank=False, null=False, )
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    password = models.CharField("Пароль", null=False, max_length=128)
    is_active = models.BooleanField("Активен", default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_user'
            )]

    def str(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribe_author',
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Нельзя подписаться на самого себя")

    def save(self, *args, **kwargs):
        self.clean()  # Выполняем проверку перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscription')
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def str(self):
        return f'{self.user} подписан на {self.author}'
