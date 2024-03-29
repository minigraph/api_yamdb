from django.core import validators
from django.db import models
from django.core.validators import RegexValidator


from users.models import CustomUser


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
        help_text='Адрес категории',
        validators=[
            RegexValidator(
                r'[-\w]+',
                'Недопустимые символы в адресе!'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'
        ordering = ('slug', )

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
        help_text='Адрес жанра',
        validators=[
            RegexValidator(
                r'[-\w]+',
                'Недопустимые символы в адресе!'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug', )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения"""

    name = models.CharField(
        'Имя',
        max_length=256,
        help_text='Название произведения',
    )

    year = models.IntegerField(
        'Год выпуска',
        null=True,
        help_text='Год создания'
    )

    description = models.TextField(
        'Описание',
        help_text='Описание',
    )

    genre = models.ManyToManyField(
        Genre,
        through='GenresOfTitles',
        related_name='titles'
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        help_text='Категория',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', )

    def __str__(self):
        return self.name


class GenresOfTitles(models.Model):
    """Жанры произведений"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Произведение',
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        ordering = ('title', 'genre')

        constraints = models.UniqueConstraint(
            fields=('title', 'genre'),
            name='title_genre',
        ),

    def __str__(self):
        return f':Жанр {self.genre} произведения {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.PositiveIntegerField(
        'Оценка',
        help_text='Оценка произведения',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10)
        ]
    )
    text = models.TextField(
        'Текст',
        help_text='Текст отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    text = models.TextField(
        'Текст',
        help_text='Текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date', )

    def __str__(self):
        return self.text
