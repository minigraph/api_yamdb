from rest_framework import serializers, validators
from reviews.models import Review
from users.models import CustomUser

from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from reviews.models import Title, Category, Genre, GenresOfTitles


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    slug = serializers.SlugField()
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
            UniqueTogetherValidator(
                queryset=GenresOfTitles.objects.all(),
                fields=['genre', 'title'],
                message='Жанр уже присвоен!'
            )
        ]


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    # при создании нового произведения передается список словарей жанров только
    # с полем slug без имени, при этом нельзя создавать новые жанры
    # с другой стороны при запросе GET необходимо
    # вернуть список словарей с полями name и slug
    # используем SerializerMethodField:
    genre = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'category', 'genre', 'name', 'description', 'year')

    def create(self, validated_data):

        # сразу создаем запись title, т.к. жанров нет в validated_data
        title = Title.objects.create(**validated_data)
        if 'genre' not in self.initial_data:
            return title
        if len(self.initial_data['genre']) == 0:
            return title
        for genre_slug in self.initial_data['genre']:
            current_genre = get_object_or_404(Genre, slug=genre_slug)
            title.genre.add(current_genre)
        title.save()
        return title

    def update(self, instance, validated_data):

        # пришли новые жанры, очищаем старые
        if 'genre' in self.initial_data:
            instance.genre.clear()

        if len(self.initial_data['genre']) == 0:
            return instance
        for genre_slug in self.initial_data['genre']:
            current_genre = get_object_or_404(Genre, slug=genre_slug)
            instance.genre.add(current_genre)
        instance.save()
        return instance

    def validate_year(self, year):
        if year > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего!'
            )
        return year

    def get_genre(self, obj):
        title = Title.objects.get(pk=obj.pk)
        genres_qs = title.genre.all()
        genres = []
        if len(genres_qs):
            for genre in genres_qs:
                genres.append({'name': genre.name, 'slug': genre.slug})
        return genres


class UserSerializer(serializers.ModelSerializer):

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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        exclude = ('title',)
        model = Review
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]
