import os

from .base import *  # noqa: F401,F403

DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() in ("1", "true", "yes", "on")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "whiteschollars"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
        "HOST": os.getenv("MYSQL_HOST", "localhost"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", "true").lower() in (
    "1",
    "true",
    "yes",
    "on",
)
CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", "true").lower() in (
    "1",
    "true",
    "yes",
    "on",
)
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "false").lower() in (
    "1",
    "true",
    "yes",
    "on",
)
