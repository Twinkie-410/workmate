from app.internal.serializers.user_serializer import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
