from django.db import models


class Category(models.Model):
    """Категории (типы) произведений"""

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


class Genre(models.Model):
    """Жанры произведений"""

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


class Title(models.Model):
    """Произведения"""

    name = models.CharField(
        'Имя',
        max_length=256,
        help_text='Название произведения',
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

    genre = models.ManyToManyField(Genre, through='GenresOfTitles')

    category = models.ForeignKey(
        Category,
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
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведение',
        help_text='Произведение',
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        ordering = ['title', 'genre']

        constraints = models.UniqueConstraint(
            fields=['title', 'genre'],
            name='title_genre',
        ),

    def __str__(self):
        return f':Жанр {self.genre} произведения {self.title}'


class Review(models.Model):
    author = models.IntegerField()  # Временно
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Оценка произведения'
    )
    text = models.TextField(
        'Текст',
        help_text='Текст отзыва'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение',
        help_text='Произведение',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
