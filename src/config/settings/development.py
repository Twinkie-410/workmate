from .base import *
from .packeges import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(hours=10)
