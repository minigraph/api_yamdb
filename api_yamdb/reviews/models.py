# from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


class Categories(models.Model):
    '''Категории (типы) произведений'''

    name = models.CharField(
        'Имя',
        max_length=256,
        help_text='Название категории',
    )

    slug = models.SlugField(
        'Адрес',
        unique=True,
        max_length=50,
        help_text='Адрес категории'
    )

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'

    def __str__(self):
        return self.name


class Genres(models.Model):
    '''Жанры'''

    name = models.CharField(
        'Имя',
        max_length=256,
        help_text='Название жанра',
    )

    slug = models.SlugField(
        'Адрес',
        unique=True,
        max_length=50,
        help_text='Адрес жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Произведения"""

    name = models.CharField(
        'Имя',
        max_length=256,
        help_text='Произведение',
    )

    year = models.DateField(
        'Год выпуска',
        null=False,
        auto_now=False,
        auto_now_add=False,
        help_text='Год выпуска'
    )

    description = models.TextField(
        'Описание',
        help_text='Описание',
    )

    genre = models.ForeignKey(
        Genres,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name='genres',
        help_text='Жанр',
        verbose_name='Жанр',
    )

    category = models.ForeignKey(
        Categories,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name='categories',
        help_text='Категория',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenresOfTitles(models.Model):
    """Жанры произведений"""

    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведения',
        help_text='Произведения',
    )

    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр',
    )

    class Meta:
        verbose_name = 'Жанры произведения'
        verbose_name_plural = 'Жанры произведения'
        ordering = ['title', 'genre']

        constraints = models.UniqueConstraint(
            fields=['title', 'genre'],
            name='title_genre',
        ),

    def __str__(self):
        return f':Жанр {self.genre} произведения {self.title}'
