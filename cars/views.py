from rest_framework import generics, permissions, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render

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
        data = request.data.copy()
        data['owner'] = request.user.id

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
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "delete", "put"]

    def get(self, request, *args, **kwargs):
        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            car = self.get_object()
            serializer = self.get_serializer(car)
            return JsonResponse(serializer.data)
        else:
            car = self.get_object()
            context = {'car': car}
            return render(request, 'retrieve.html', context)

    def put(self, request, *args, **kwargs):
        # Update car details via AJAX (PUT request)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            car = self.get_object()
            data = request.data
            serializer = self.get_serializer(car, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse({"error": "Invalid data"}, status=400)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete car via AJAX (DELETE request)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            car = self.get_object()
            car.delete()

            return JsonResponse({"message": "Car deleted successfully"})
        return super().delete(request, *args, **kwargs)
    # def perform_create(self, serializer):
    #     """
    #      Метод для сохранения владельца машины при создании.
    #      """
    #     serializer.save(owner=self.request.user)
    #


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
