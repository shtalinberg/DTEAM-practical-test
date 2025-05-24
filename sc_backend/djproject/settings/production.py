import os

import dj_database_url

from .base_django import *

DEBUG = False


DATABASES = (
    {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
    if os.environ.get('DATABASE_URL')
    else {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('POSTGRES_DB', 'dteam'),
            "USER": os.environ.get('POSTGRES_USER', 'dteam'),
            "PASSWORD": os.environ.get('POSTGRES_PASSWORD', 'dteam2025'),
            "HOST": os.environ.get('POSTGRES_HOST', 'localhost'),
            "PORT": os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
)

SECURE_SSL_REDIRECT = False  # will be Set to True if using HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
