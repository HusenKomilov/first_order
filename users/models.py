from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    full_name = models.CharField(max_length=256, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "full_name"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def tokens(self):
        pass

    class Meta:
        swappable = "AUTH_USER_MODEL"
