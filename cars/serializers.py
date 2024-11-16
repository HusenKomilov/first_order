from rest_framework import serializers

from users.models import User
from .models import Comment, Car


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name")


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content", "car", "author", "created_at")


class CarSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "year", "description", "owner", "comment")
