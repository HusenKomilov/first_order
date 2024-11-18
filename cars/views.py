from rest_framework import generics, permissions

from cars.models import Car, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import CarSerializer, CommentSerializer


class CarListAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.accepted_renderer.format == 'html':
            return Response({'cars': queryset})

        return Response(self.get_serializer(queryset, many=True).data)

    def post(self, request, *args, **kwargs):
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        car_id = self.kwargs['pk']
        return Comment.objects.filter(car=car_id)

    def perform_create(self, serializer):
        car_id = self.kwargs['pk']
        serializer.save(author=self.request.user, car_id=car_id)
