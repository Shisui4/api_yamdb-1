from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=20,
        choices=(('moderator','m'), ('admin','a'), ('user','u')),
        default='user'
    )

    def __str__(self):
        return self.username
