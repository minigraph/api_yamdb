from api.permissions import AdminOrReadOnly, AuthorOrStaffOrReadOnly, IsAdmin
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser

from .serializers import (CheckCodeSerializer, CommentSerializer,
                          ReviewSerializer, UserSerializer)


class CategoryViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin,
                      mixins.CreateModelMixin, mixins.ListModelMixin):
    """Вьюсет категорий."""

    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin,
                   mixins.CreateModelMixin, mixins.ListModelMixin):
    """Вьюсет жанров произведений."""

    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(mixins.DestroyModelMixin,
                   mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет произведений."""

    permission_classes = [
        AdminOrReadOnly,
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
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    # Создаёт эндпоинт "me" и позволяет работать со своим объектом
    # и только авторизованному пользователю
    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Посмотреть и отредактировать данные своего профиля"""
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def send_confirmation_code(request):
    """Отправляет код подтверждения на почту (в локальную папку)"""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    username = request.data.get('username')
    user, created = CustomUser.objects.get_or_create(
        email=email,
        username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации',
        (f'Ваш код подтверждения: {confirmation_code}'),
        'admin@api_yamdb.com',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data)


@api_view(['POST'])
def get_jwt_token(request):
    """Получение и обновление токена"""
    serializer = CheckCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=request.data.get('username')
    )
    confirmation_code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = AccessToken.for_user(user)
        return Response({'token': str(jwt_token)})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (AuthorOrStaffOrReadOnly,)

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
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def __get_review(self):
        """Получить экземпляр Review по id из пути."""
        id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())

    def get_queryset(self):
        return self.__get_review().comments.all()
