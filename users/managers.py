from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, full_name, password=None, **extra_fields):
        if not full_name:
            raise ValueError("Enter your full_name")

        user = self.model(full_name=full_name)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, full_name, password, **extra_fields):
        user = self.create_user(full_name=full_name, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self.db)
        return user
