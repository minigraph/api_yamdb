from django.shortcuts import get_object_or_404
from reviews.models import Review, Title
from rest_framework import viewsets, pagination
from . import serializers


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.PageNumberPagination

    def __get_title(self):
        """Получить экземпляр Title по id из пути."""
        id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=id)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user, title=self.__get_title())

    # def get_queryset(self):
    #     return self.__get_title().reviews.all()
