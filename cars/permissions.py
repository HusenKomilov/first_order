from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешение, которое позволяет только автору объекта выполнять модификации (PUT, DELETE),
    в то время как остальные пользователи могут только просматривать (GET, HEAD, OPTIONS).
    """
    def has_object_permission(self, request, view, obj):
        """
        Метод для проверки, есть ли у пользователя разрешение для доступа к объекту.
        Проверяется метод запроса и авторство объекта.
        """
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return obj.owner == request.user
