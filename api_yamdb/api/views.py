from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import pagination, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title
from users.models import CustomUser

from .serializers import ReviewSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def send_confirmation_code(request):
    """Отправляет код подтверждения на почту (в локальную папку)"""
    email = request.data.get('email')
    user, created = CustomUser.objects.get_or_create(
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации',
        (f'Ваш код подтверждения: {confirmation_code}'),
        'admin@api_yamdb.com',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({'email': email})


@api_view(['POST'])
def get_jwt_token(request):
    """Получение и обновление токена"""
    user = get_object_or_404(
        CustomUser,
        email=request.data.get('email')
    )
    confirmation_code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = RefreshToken.for_user(user)
        return Response({'token': str(jwt_token)})
    return Response('Неверный код или e-mail')


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
