from rest_framework import serializers, validators
from reviews.models import Review
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True,
        validators=[validators.UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=CustomUser.objects.all())]
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
    extra_kwargs = {'confirmation_code': {'write_only': True}}

# Запрет на использование "me" в качестве username
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя зарегистрировать пользователя с таким именем!')
        return value


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
