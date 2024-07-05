from .base import *
from .packeges import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["NAME"],
        "USER": os.environ["USER"],
        "PASSWORD": os.environ["PASSWORD"],
        "HOST": os.environ["HOST"],
        "PORT": os.environ["PORT"],
    }
}
