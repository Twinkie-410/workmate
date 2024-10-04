import jwt
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from jwt import DecodeError, ExpiredSignatureError
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.internal.serializers.auth_serializer import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    RequestResetPasswordSerializer,
    SetNewPasswordSerializer,
    UserRegisterSerializer,
)
from app.internal.utils.mailings.notify_change_password_email import notify_change_password
from app.internal.utils.mailings.reset_password_email import send_reset_password_email
from app.internal.utils.mailings.send_confirm_email import send_confirm_email
from config import settings


class UserRegisterAPIView(CreateAPIView):
    """Registers the user in the system and sends a confirmation email"""

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        send_confirm_email(serializer.data, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmailConfirmAPIView(APIView):
    """Confirms email: sets the-verify field to true"""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "token",
                in_=openapi.IN_QUERY,
                description="Access token",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        try:
            payload = jwt.decode(
                request.query_params.get("token"), settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT["ALGORITHM"]
            )

            user = get_user_model().objects.get(id=payload["user_id"])
            user.is_verified = True
            user.email = request.query_params.get("change-to").lower()
            user.save()

            return Response({"OK": "Successfully activated"}, status=status.HTTP_200_OK)

        except DecodeError:
            return Response({"ERROR": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except ExpiredSignatureError:
            return Response({"ERROR": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailAPIView(GenericAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_confirm_email(request.user.__dict__, request, serializer.data["email"])
        return Response({"OK": "We have sent you an email, please confirm new email"})


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        username = user_data["username"]

        user = get_user_model().objects.get(username=username)
        if not user.is_verified:
            send_confirm_email(user.__dict__, request)

            return Response(
                {"OK": f"Hello, {username}! We sent you a confirmation email"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        refresh = request.data
        serializer = self.serializer_class(data=refresh)
        serializer.is_valid(raise_exception=True)

        return Response({"OK": "Goodbye!"}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        notify_change_password(request.user.__dict__, request)
        return Response({"OK": "Password change is successful"}, status=status.HTTP_200_OK)


class RequestResetPasswordAPIView(GenericAPIView):
    serializer_class = RequestResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        send_reset_password_email(user.__dict__, request)
        return Response({"OK": "We have sent you a link to reset your password"})


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")

        serializer = self.get_serializer(data=request.data, context={"uidb64": uidb64, "token": token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"OK": "Password change is successful"})
