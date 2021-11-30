from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=20,
        choices=(('m','moderator'), ('a','admin'), ('u','user')),
        default='user'
    )

    def __str__(self):
        return self.username
