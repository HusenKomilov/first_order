from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    # Поле password только для записи, минимальная длина пароля 8 символов

    class Meta:
        model = User  # Модель пользователя, с которой связан этот сериализатор
        fields = ('id', 'full_name', 'password')  # Поля для сериализации

    def create(self, validated_data):
        # Метод для создания пользователя в базе данных

        user = User.objects.create_user(
            full_name=validated_data['full_name'],  # Имя пользователя
            password=validated_data['password']  # Пароль пользователя
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для авторизации пользователя.
    """
    full_name = serializers.CharField()  # Поле для ввода имени пользователя
    password = serializers.CharField(write_only=True)  # Поле для ввода пароля

    def validate(self, data):
        # Метод для валидации данных при попытке входа
        user = authenticate(
            full_name=data.get('full_name'),  # Попытка найти пользователя по имени
            password=data.get('password')  # И проверка пароля
        )
        if not user:
            # Если пользователя не найдено или неверный пароль
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            # Если пользователь не активен (например, аккаунт заблокирован)
            raise serializers.ValidationError("User is inactive")

        # Возвращаем пользователя, если аутентификация прошла успешно
        return user
