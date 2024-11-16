from django.urls import path

from cars import views

urlpatterns = [
    path("cars/", views.CarListAPIView.as_view(), name="cars_list"),
    path("comments/<int:id>/", views.CommentListAPIView().as_view(), name="comments_list_create"),
]
