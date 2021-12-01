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


class Categories(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Категория',
                            unique=True)
    slug = models.SlugField(max_length=20,
                            unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Жанр',
                            unique=True)
    slug = models.SlugField(max_length=20,
                            unique=True,
                            )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=50,)
    release = models.IntegerField('Дата выпуска')
    description = models.TextField(max_length=200)
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   null=True)
    categories = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
