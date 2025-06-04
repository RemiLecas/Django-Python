from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("PROD_DB_NAME"),
        'USER': os.getenv("PROD_DB_USER"),
        'PASSWORD': os.getenv("PROD_DB_PASSWORD"),
        'HOST': os.getenv("PROD_DB_HOST"),
        'PORT': os.getenv("PROD_DB_PORT", "5432"),
    }
}
