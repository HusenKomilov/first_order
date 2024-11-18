from rest_framework import generics, permissions, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from cars.models import Car, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import CarSerializer, CommentSerializer


class CarListAPIView(generics.ListCreateAPIView):
    """
    Класс для получения списка машин и создания новой машины.
    Это комбинированный API, который обрабатывает запросы GET и POST.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Метод GET для получения списка машин.
        В зависимости от типа контента (HTML или JSON) возвращаем соответствующий ответ.
        """
        queryset = self.get_queryset()

        if request.accepted_renderer.format == 'html':
            return Response({'cars': queryset})

        return Response(self.get_serializer(queryset, many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Метод POST для создания новой машины.
        Принимает данные, валидирует и сохраняет новую машину в базе данных.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.accepted_renderer.format == 'html':
                queryset = self.get_queryset()
                return Response({'cars': queryset, 'success': True}, template_name=self.template_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.accepted_renderer.format == 'html':
            queryset = self.get_queryset()
            return Response({'cars': queryset, 'errors': serializer.errors}, template_name=self.template_name)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Класс для получения, обновления или удаления конкретной машины.
    Используется для обработки запросов GET, PUT и DELETE.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "delete", "put"]

    def perform_create(self, serializer):
        """
         Метод для сохранения владельца машины при создании.
         """
        serializer.save(owner=self.request.user)


class CommentListAPIView(generics.ListCreateAPIView):
    """
    Класс для получения списка комментариев и создания нового комментария для конкретной машины.
    Это комбинированный API, который обрабатывает запросы GET и POST.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Метод для получения списка комментариев для конкретной машины.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        car_id = self.kwargs['pk']
        return Comment.objects.filter(car=car_id)

    def perform_create(self, serializer):
        """
        Метод для сохранения комментария, добавляя автора и машину, к которой он относится.
        """
        car_id = self.kwargs['pk']
        serializer.save(author=self.request.user, car_id=car_id)


