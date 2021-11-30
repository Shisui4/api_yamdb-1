from django.contrib.auth.models import AbstractUser
from django.db import  models



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


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields = ('title', 'author',),
                name = 'unique_titles_author'
            ),
        )
    
    def __str__(self):
        return self.text




# индексы сортируют ваши данные по тому полю, для которого вы укажете db_index=True,
# а искать по сортированным данным получается быстрее, нежели простым перебором всего подряд.
# Указывайте этот параметр, чтобы создать индекс для поля, по которому вы совершаете поисковые запросы.
# Так как индексы хранятся отдельно, их можно создавать для нескольких полей.
