from django.urls import path

from app.internal.views.user_view import UserDetailAPIView, UserListAPIView

urlpatterns = [
    path("list/", UserListAPIView.as_view(), name="users"),
    path("me/", UserDetailAPIView.as_view(), name="user-detail"),
]
