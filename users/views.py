from django.contrib.auth import logout, login
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    """
    Класс для регистрации пользователя.
    """

    def get(self, request):
        # Метод GET возвращает HTML-страницу для регистрации пользователя.
        return render(request, 'registration.html')

    def post(self, request):
        # Метод POST обрабатывает данные формы регистрации.
        # При успешной валидации данных создается новый пользователь.
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        # Если данные некорректны, возвращается ошибка с описанием.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Класс для авторизации пользователя.
    """

    def get(self, request):
        # Метод GET проверяет, авторизован ли пользователь.
        # Если пользователь уже вошел в систему, перенаправляет его на страницу с машинами.
        if request.user.is_authenticated:
            return redirect("cars_list")
        # Если пользователь не авторизован, возвращает страницу входа.
        return render(request, "login.html")

    def post(self, request):
        # Метод POST обрабатывает данные формы входа.
        # При успешной валидации данных пользователь авторизуется и перенаправляется на страницу с машинами.
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)  # Создание refresh token для пользователя
            login(request, user)  # Вход пользователя в систему
            return redirect("cars_list")

        # Если данные некорректны, возвращается ошибка с описанием.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_logout(request):
    """
    Функция для выхода пользователя из системы.
    """
    logout(request)
    return redirect("cars_list")


class JWTModelBackend(ModelBackend):
    """
    Класс для аутентификации пользователей с использованием JWT (JSON Web Token).
    """

    def authenticate(self, request, token=None):
        # Метод для аутентификации пользователя по токену JWT.
        if token is None:
            return None

        jwt_auth = JWTAuthentication()  # Создание объекта для аутентификации через JWT
        user, auth_token = jwt_auth.authenticate(request)  # Аутентификация пользователя с использованием токена

        # Если пользователь найден и является администратором (is_staff), возвращается его объект.
        if user and user.is_staff:
            return user
        # Если пользователь не является администратором или аутентификация не удалась, возвращается None.
        return None
