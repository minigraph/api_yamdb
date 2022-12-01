from rest_framework import serializers
from users.models import CustomUser, Review


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

    class Meta:
        exclude = ('title',)
        model = Review
