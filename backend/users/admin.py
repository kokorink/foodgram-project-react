"""Описание модели пользователя и подписок для админ-зоны."""

from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    """Представление модели User."""

    list_display = ('id',
                    'username',
                    'email',
                    'role',
                    'first_name',
                    'last_name'
                    )
    list_editable = ('role',)
    search_fields = ('username', 'first_name', 'last_name',)
    list_display_links = ('username',)


class SubscriptionAdmin(admin.ModelAdmin):
    """Представление модели для подписок."""

    list_display = ('user', 'author')
    ordering = ('user',)
    search_fields = ('user', 'author')
    list_display_links = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
