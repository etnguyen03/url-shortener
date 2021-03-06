import os
import sys
from typing import Dict, List

import sentry_sdk
from celery.schedules import crontab
from django.urls import reverse_lazy
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = True

TESTING = "test" in sys.argv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "*-fuslvu#e=#8+5)o9e+y_#vo$wu8=gx@b9v*yp!e_p%0afvr9"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "tiny.tjhsst.edu",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "social_django",
    "shortener.apps",
    "shortener.apps.auth.apps.AuthConfig",
    "shortener.apps.urls.apps.UrlsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shortener.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "shortener.apps.context_processors.base_context",
            ],
        },
    },
]

WSGI_APPLICATION = "shortener.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

if TESTING:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
    DATABASES["default"]["NAME"] = ":memory:"

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "authentication.User"

AUTHENTICATION_BACKENDS: List[str] = ["shortener.apps.auth.oauth.IonOauth2"]

SOCIAL_AUTH_USER_FIELDS = [
    "username",
    "first_name",
    "last_name",
    "email",
    "id",
    "is_student",
    "is_teacher",
    "is_staff",
    "is_superuser",
]
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
)
SOCIAL_AUTH_ALWAYS_ASSOCIATE = True
SOCIAL_AUTH_LOGIN_ERROR_URL = reverse_lazy("auth:error")
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


LOGIN_URL = reverse_lazy("auth:login")
LOGIN_REDIRECT_URL = reverse_lazy("urls:create")
LOGOUT_REDIRECT_URL = reverse_lazy("auth:login")

SESSION_SAVE_EVERY_REQUEST = True

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "serve")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Celery
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_TIMEZONE = "America/New_York"
CELERY_BEAT_SCHEDULE = {
    "delete-old-games": {
        "task": "shortener.apps.urls.tasks.delete_old_urls",
        "schedule": crontab(month_of_year=6),
        "args": (),
    }
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"format": "{asctime}:{module}:{levelname} {message}", "style": "{"},
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/info.log"),
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "shortener": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Shortener
DEFAULT_SLUG_LENGTH = 10  # characters

# Mail
MAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.tjhsst.edu"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = "[Shortener]"
EMAIL_FROM = "shortener-noreply@tjhsst.edu"
FORCE_EMAIL_SEND = True
DEVELOPER_EMAIL = "sysadmins@tjhsst.edu"

try:
    from .secret import *  # noqa
except ImportError:
    DEBUG = True
    SENTRY_DSN = ""


if not DEBUG:
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        send_default_pii=True,
    )
