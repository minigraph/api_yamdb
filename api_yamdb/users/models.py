from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class CustomUser(AbstractUser):
    """Переопределяем модель пользователя, добавив необходимые поля"""
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        null=False
    )
    role = models.CharField(
        'Права доступа',
        max_length=20,
        choices=ROLES
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
