from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DEV_DB_NAME", "blog_dev"),
        'USER': os.getenv("DEV_DB_USER", "postgres"),
        'PASSWORD': os.getenv("DEV_DB_PASSWORD", ""),
        'HOST': os.getenv("DEV_DB_HOST", "localhost"),
        'PORT': os.getenv("DEV_DB_PORT", "5432"),
    }
}
