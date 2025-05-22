from .base_localdev import *

DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = False
TESTS_IN_PROGRESS = True

# to SQLite memory
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "TEST": {"MIGRATE": False},
}
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

INSTALLED_APPS = tuple(
    [
        x
        for x in INSTALLED_APPS
        if x
        not in [
            "debug_toolbar",
        ]
    ]
)

MIDDLEWARE = tuple(
    [
        x
        for x in MIDDLEWARE
        if x
        not in [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]
    ]
)
