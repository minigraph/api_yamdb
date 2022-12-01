from django.shortcuts import get_object_or_404
from rest_framework import viewsets, pagination
from reviews.models import Review, Title
from users.models import CustomUser

from .serializers import UserSerializer, ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination

    def __get_title(self):
        """Получить экземпляр Title по id из пути."""
        id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, titles=self.__get_title())

    def get_queryset(self):
        return self.__get_title().reviews.all()
