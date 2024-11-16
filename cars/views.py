from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from cars.models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class CarListAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "delete", "put"]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs['pk']
        return Comment.objects.filter(car=car_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
