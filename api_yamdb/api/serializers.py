from datetime import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from reviews.models import (Category, Comment, Genre, GenresOfTitles, Review,
                            Title)
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    slug = serializers.SlugField(
        validators=[validators.UniqueValidator(
            queryset=Category.objects.all()
        )])

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    slug = serializers.SlugField(
        validators=[validators.UniqueValidator(
            queryset=Genre.objects.all()
        )])
    name = serializers.CharField(required=False)

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class GenresOfTitlesSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',

    )

    class Meta:
        fields = ('genre', 'title')
        model = GenresOfTitles

        validators = [
            validators.UniqueTogetherValidator(
                queryset=GenresOfTitles.objects.all(),
                fields=['genre', 'title'],
                message='Жанр уже присвоен!'
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    # при создании нового произведения передается список словарей жанров только
    # с полем slug без имени, при этом нельзя создавать новые жанры
    # с другой стороны при запросе GET необходимо
    # вернуть список словарей с полями name и slug
    # используем SerializerMethodField:
    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(
    #     queryset=Category.objects.all(),
    #     slug_field='slug',
    # )
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'category', 'genre', 'name', 'description', 'year', 'rating'
        )

    def create(self, validated_data):

        # сразу создаем запись title, т.к. жанров нет в validated_data
        title = Title.objects.create(**validated_data)
        if 'genre' in self.initial_data:
            data_genre = self.initial_data.getlist('genre', [])
            for genre_slug in data_genre:
                current_genre, _ = Genre.objects.get_or_create(slug=genre_slug)
                title.genre.add(current_genre)

        if 'category' in self.initial_data:
            category = Category.objects.filter(
                slug=self.initial_data['category']
            ).get()
            if category:
                title.category = category
        title.save()
        return title

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name')
        instance.year = validated_data.get('year')

        # пришли новые жанры, очищаем старые
        if 'genre' in self.initial_data:
            instance.genre.clear()

        if 'genre' in self.initial_data:
            for genre_slug in self.initial_data['genre']:
                current_genre, _ = Genre.objects.get_or_create(slug=genre_slug)
                instance.genre.add(current_genre)

        if 'category' in self.initial_data:
            category = Category.objects.filter(
                slug=self.initial_data['category']
            ).get()
            if category:
                instance.category = category
        instance.save()
        return instance

    def validate_year(self, year):
        if year > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего!'
            )
        return year

    def get_category(self, obj):
        return {'name': obj.category.name, 'slug': obj.category.slug}

    def get_genre(self, obj):
        # title = Title.objects.get(pk=obj.pk)
        genres_qs = obj.genre.all()
        genres = []
        if len(genres_qs):
            for genre in genres_qs:
                genres.append({'name': genre.name, 'slug': genre.slug})
        return genres

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(result=Avg('score'))
        if rating['result'] is None:
            return None
        return int(rating['result'])


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
    extra_kwargs = {
        'confirmation_code': {'write_only': True}
    }

# Запрет на использование "me" в качестве username
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя зарегистрировать пользователя с таким именем!')
        return value


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context['view']
        return get_object_or_404(Title, id=view.kwargs['title_id'])

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=CurrentTitleDefault()
    )

    class Meta:
        fields = ('id', 'author', 'pub_date', 'score', 'text', 'title')
        model = Review
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        exclude = ('review',)
        model = Comment
