from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_admin",
            "is_staff",
            "is_active",
            "is_verified",
        ]

        read_only_fields = [
            "id",
            "email",
            "date_joined",
            "is_admin",
            "is_staff",
            "is_active",
            "is_verified",
        ]
