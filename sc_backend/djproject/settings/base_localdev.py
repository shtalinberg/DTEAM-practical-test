import sys

from .base_django import *

DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

TESTING_MODE = len(sys.argv) > 1 and sys.argv[1] == "test"
RUNLOCAL_MODE = len(sys.argv) > 1 and sys.argv[1] == "runserver"
SSLIFY_DISABLE = True
SECURE_SSL_REDIRECT = False


EMAIL_SUBJECT_PREFIX = "[local] "
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(REPOSITORY_ROOT, "help-man/emails")

if TESTING_MODE:
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
