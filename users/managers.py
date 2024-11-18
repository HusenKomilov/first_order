from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Менеджер для управления пользователями.
    Это кастомизированный менеджер, который используется для создания пользователей и суперпользователей.
    """
    def create_user(self, full_name, password=None, **extra_fields):
        """
        Метод для создания обычного пользователя.
        Принимает имя пользователя и пароль.
        """
        if not full_name:
            raise ValueError("Enter your full_name")

        user = self.model(full_name=full_name)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, full_name, password, **extra_fields):
        """
        Метод для создания суперпользователя (администратора).
        В дополнение к обычному пользователю, он делает пользователя суперпользователем и администратором.
        """
        user = self.create_user(full_name=full_name, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self.db)
        return user
