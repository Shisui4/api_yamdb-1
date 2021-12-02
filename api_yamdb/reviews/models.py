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
        choices=(('moderator', 'm'), ('admin', 'a'), ('user', 'u')),
        default='user'
    )
    confirmation_code = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True,
        null=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True,
        null=False
    )
    score = models.PositiveSmallIntegerField(null=False)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True,
        null=False
    )
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True,
        null=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
