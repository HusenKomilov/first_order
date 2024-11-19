from rest_framework import serializers

from users.models import User
from .models import Comment, Car


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Этот сериализатор конвертирует данные модели User в формат, который можно передать через API.
    """

    class Meta:
        model = User
        fields = ("id", "full_name")


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели комментария.
    Этот сериализатор будет использоваться для конвертации комментариев в формат, который можно вернуть в ответе API.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content", "car", "author", "created_at")


class CarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели машины.
    Этот сериализатор будет использоваться для конвертации машин в формат, который можно вернуть в ответе API.
    """
    comment = CommentSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "year", "description", "owner", "comment")

    def create(self, validated_data):
        # Automatically set the owner as the logged-in user
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
