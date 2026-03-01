import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def _env_int(name, default):
    raw_value = os.getenv(name, str(default)).strip()
    try:
        return int(raw_value)
    except ValueError as exc:
        raise ImproperlyConfigured(f"{name} must be an integer, got: {raw_value!r}") from exc


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-me-in-production",
)
if SECRET_KEY == "django-insecure-change-me-in-production":
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY.")

DEBUG = _env_bool("DJANGO_DEBUG", False)
DJANGO_ENV = "production"

ALLOWED_HOSTS = ["api.whitescholars.com", "127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["https://api.whitescholars.com"]

mysql_database = os.getenv("MYSQL_DATABASE", "").strip()
mysql_user = os.getenv("MYSQL_USER", "").strip()
mysql_password = os.getenv("MYSQL_PASSWORD", "").strip()

if not mysql_database or not mysql_user or not mysql_password:
    raise ImproperlyConfigured(
        "Set MYSQL_DATABASE, MYSQL_USER, and MYSQL_PASSWORD."
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": mysql_database,
        "USER": mysql_user,
        "PASSWORD": mysql_password,
        "HOST": os.getenv("MYSQL_HOST", "localhost"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "CONN_MAX_AGE": _env_int("MYSQL_CONN_MAX_AGE", 120),
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

WSGI_APPLICATION = 'myproject.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = _env_bool("DJANGO_USE_X_FORWARDED_HOST", True)
SESSION_COOKIE_SECURE = _env_bool("DJANGO_SESSION_COOKIE_SECURE", True)
SESSION_COOKIE_HTTPONLY = _env_bool("DJANGO_SESSION_COOKIE_HTTPONLY", True)
SESSION_COOKIE_SAMESITE = os.getenv("DJANGO_SESSION_COOKIE_SAMESITE", "Lax")
CSRF_COOKIE_SECURE = _env_bool("DJANGO_CSRF_COOKIE_SECURE", True)
CSRF_COOKIE_HTTPONLY = _env_bool("DJANGO_CSRF_COOKIE_HTTPONLY", True)
CSRF_COOKIE_SAMESITE = os.getenv("DJANGO_CSRF_COOKIE_SAMESITE", "Lax")
SECURE_SSL_REDIRECT = _env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
SECURE_HSTS_SECONDS = _env_int("DJANGO_SECURE_HSTS_SECONDS", 3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = _env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
SECURE_CONTENT_TYPE_NOSNIFF = _env_bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", True)
SECURE_REFERRER_POLICY = os.getenv(
    "DJANGO_SECURE_REFERRER_POLICY",
    "strict-origin-when-cross-origin",
)
X_FRAME_OPTIONS = os.getenv("DJANGO_X_FRAME_OPTIONS", "DENY")

DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO").strip().upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": DJANGO_LOG_LEVEL,
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
    },
}
