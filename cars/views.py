from rest_framework import generics, permissions

from cars.models import Car, Comment
from .serializers import CarSerializer, CommentSerializer


class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs.get("id")
        return Comment.objects.filter(car=car_id)
