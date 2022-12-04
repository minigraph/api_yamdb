from django.shortcuts import get_object_or_404
from rest_framework import viewsets, pagination
from reviews.models import Review, Title
from users.models import CustomUser

from .serializers import UserSerializer, ReviewSerializer, CommentSerializer


from rest_framework import viewsets
from rest_framework import filters

from api.serializers import CategorySerializer, GenreSerializer
from api.serializers import TitleSerializer
from api.permissions import IsAdministratorOrReadinly
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий."""

    # Заменить на реальные классы!
    permission_classes = [
        IsAdministratorOrReadinly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_object(self):
        return Category.objects.get(slug=self.kwargs['pk'])


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет жанров произведений."""

    # Заменить на реальные классы!
    permission_classes = [
        IsAdministratorOrReadinly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_object(self):
        return Genre.objects.get(slug=self.kwargs['pk'])


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""

    # Заменить на реальные классы!
    permission_classes = [
        IsAdministratorOrReadinly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'name', 'year')

    def get_object(self):
        return Title.objects.get(pk=self.kwargs['pk'])


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination

    def __get_title(self):
        """Получить экземпляр Title по id из пути."""
        id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.__get_title())

    def get_queryset(self):
        return self.__get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination

    def __get_review(self):
        """Получить экземпляр Review по id из пути."""
        id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())

    def get_queryset(self):
        return self.__get_review().comments.all()
