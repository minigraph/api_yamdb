from django.shortcuts import get_object_or_404
from rest_framework import viewsets, pagination
from reviews.models import Review, Title
from users.models import CustomUser

from .serializers import UserSerializer, ReviewSerializer, CommentSerializer


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
