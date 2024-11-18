from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.backends import ModelBackend

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    def get(self, request):
        # HTML sahifaga yo'naltirish
        return render(request, 'registration.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("cars_list")
        return render(request, "login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            login(request, user)
            return redirect("cars_list")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_logout(request):
    logout(request)
    return redirect("cars_list")


class JWTModelBackend(ModelBackend):
    def authenticate(self, request, token=None):
        if token is None:
            return None

        jwt_auth = JWTAuthentication()
        user, auth_token = jwt_auth.authenticate(request)

        if user and user.is_staff:
            return user
        return None
