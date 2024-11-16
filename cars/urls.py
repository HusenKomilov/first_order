from django.urls import path

from cars import views

urlpatterns = [
    path("", views.CarListAPIView.as_view(), name="cars_list"),
    path("<int:pk>/", views.CarRetrieveUpdateDestroyAPIView.as_view(), name="cars_retrieve"),
    path("<int:pk>/comments/", views.CommentListAPIView().as_view(), name="comments_list_create"),
]
