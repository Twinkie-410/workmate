from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data.pop("username"),
            email=validated_data.pop("email").lower(),
            is_verified=validated_data.pop("is_verified") if "is_verified" in validated_data else False,
        )
        user.set_password(validated_data.pop("password"))
        super().update(user, validated_data)
        return user

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"ERROR": "Пароли не совпадают"})

        return attrs

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "date_joined",
            "is_admin",
            "is_staff",
            "is_active",
            "is_verified",
        ]

        read_only_fields = ["id", "license_period", "date_joined", "is_admin", "is_staff", "is_active", "is_verified"]


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            raise ValidationError({"ERROR": "This email is already registered"}, 400)

        return attrs


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = get_user_model().objects.get(username=obj["username"])
        refresh = RefreshToken.for_user(user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    class Meta:
        model = get_user_model()
        fields = ["username", "password", "tokens"]

    def validate(self, attrs):
        user_obj = (
            get_user_model().objects.filter(email=attrs.get("username")).first()
            or get_user_model().objects.filter(username=attrs.get("username")).first()
        )

        if user_obj:
            credentials = {"username": user_obj.username, "password": attrs.get("password")}
        else:
            raise AuthenticationFailed("Неверное имя пользователя или неверный адрес электронный почты")

        user = authenticate(username=credentials["username"], password=credentials["password"])
        if not user:
            raise AuthenticationFailed("Неверный пароль, попробуйте снова")
        if not user.is_active:
            raise AuthenticationFailed("Аккаунт отключён, свяжитесь с администратором")

        return {
            "email": user.email,
            "username": user.username,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)
    token_class = RefreshToken

    def validate(self, attrs):
        try:
            refresh = self.token_class(attrs["refresh"])
        except TokenError:
            raise ValidationError("Invalid token")

        refresh.blacklist()
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"ERROR": "Старый пароль неверный"}, 403)

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"ERROR": "Пароли не совпадают"}, 403)

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()


class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        user = get_user_model().objects.filter(email=attrs["email"]).first()
        if user is None:
            raise ValidationError({"ERROR": "This email isn't registered"}, 404)

        return user


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        uidb64 = self.context["uidb64"]
        token = self.context["token"]
        if uidb64 and token:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)
        else:
            raise serializers.ValidationError({"ERROR": "uid or token invalid"}, 400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"ERROR": "Token is not valid, please request a new one"}, 400)

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"ERROR": "Пароли не совпадают"}, 403)

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
