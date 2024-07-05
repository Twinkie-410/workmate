from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # first_name
    # last_name
    email = models.EmailField(blank=False, null=True, unique=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
