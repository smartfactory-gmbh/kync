"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from copy import deepcopy

from django.utils.log import DEFAULT_LOGGING
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .utils import generate_secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set casting, default values
environ.Env.BOOLEAN_TRUE_STRINGS = ("true", "on", "ok", "y", "yes", "1", "True")
env = environ.Env(PRODUCTION=(bool, False), TEST=(bool, False))

# Load .env file
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)
    print("Env file found and loaded")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="")

if SECRET_KEY == "":
    print("Warning! No secret key found. Using a one-shot generated key.")
    print("Please setup a SECRET_KEY value in your .env file.")
    SECRET_KEY = generate_secret()

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = env("PRODUCTION")
TEST = env("TEST")
DEV = not PRODUCTION and not TEST
DEBUG = env.bool("DEBUG", default=False)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third party apps
    "debug_toolbar",
    "django_filters",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    # Project apps
    "project",
    "custom_auth",
    "sync",
]

MIDDLEWARE = [
    "project.middlewares.HealthCheckMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "project.middlewares.IPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "project.middlewares.ProfilerMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DB_USER = env.str("POSTGRES_USER", default="")
DB_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
DB_NAME = env.str("POSTGRES_DB", default="")
DB_HOST = env.str("POSTGRES_HOST", default="")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DEFAULT_DB_STRING = f"psql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

DATABASES = {"default": env.db("DATABASE_URL", default=DEFAULT_DB_STRING)}

# HTTP Security (CORS, CSRF, etc.)
X_FRAME_OPTIONS = "DENY"
ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", default="*").split(",")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# When using nginx as a proxy, the project should use the forwarded host header.
# This could mess with CSRF for instance when not set
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST", default=DEV)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
]
if DEBUG:
    CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

# Error tracking
SENTRY_SKIP = env.bool("SENTRY_SKIP", default=DEV)
SENTRY_DSN = env.str("SENTRY_DSN", None)

if not SENTRY_SKIP and SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[DjangoIntegration()],
        auto_session_tracking=False,
        release=env.str("RELEASE"),
        environment="PROD" if PRODUCTION else "TEST" if TEST else "DEV",
    )

# Authentication
AUTH_USER_MODEL = "custom_auth.User"
AUTHENTICATION_BACKENDS = ("custom_auth.backends.EmailOrUsernameModelBackend",)
ADMINS = [("Project name Admin", "webdev+project_name@smartfactory.ch")]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
FORMAT_MODULE_PATH = ["project.formats"]

# Static files (CSS, JavaScript, Images)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# E-mail
EMAIL_HOST = env.str("SMTP_HOST", "smtp.gmail.com")
EMAIL_HOST_PASSWORD = env.str("SMTP_PASSWORD", "no_pass")  # Set password in .env
EMAIL_HOST_USER = env.str("SMTP_USERNAME", "no-reply@smartfactory.ch")
EMAIL_PORT = env.int("SMTP_PORT", 587)
EMAIL_USE_TLS = env.bool("SMTP_USE_TLS", True)
DEFAULT_FROM_EMAIL = env.str("EMAIL_SENDER_ADDRESS", EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # used by internal django email (server alerts to ADMINS)

EMAIL_USE_CONSOLE_BACKEND = env.bool("EMAIL_USE_CONSOLE_BACKEND", DEV)

if EMAIL_USE_CONSOLE_BACKEND:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Caching
REDIS_HOST = env.str("REDIS_HOST", None)
if REDIS_HOST:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://{REDIS_HOST}:6379",
        }
    }

# Using redis as default session storage (avoid DB hits)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Django messages framework
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Logging
logging_dict = deepcopy(DEFAULT_LOGGING)
del logging_dict["handlers"]["mail_admins"]
del logging_dict["handlers"]["console"]["filters"]
logging_dict["loggers"]["django"]["handlers"] = ["console"]
LOGGING = logging_dict


# Django debug toolbar
if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


def show_toolbar(request):
    # Disable toolbar for DEBUG=False or python manage.py test
    if not DEBUG or sys.argv[1:2] == ["test"]:
        return False
    return request.META.get("REMOTE_ADDR") in INTERNAL_IPS


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "project.settings.show_toolbar",
}

# Rosetta
ROSETTA_UWSGI_AUTO_RELOAD = True

# Pipeline info
try:
    PIPELINE_ID = env.int("PIPELINE_ID", 0)
except ValueError:
    PIPELINE_ID = 0

# SSH config

SSH_KEYPAIR_LOCATION = env.path("SSH_KEYPAIR_LOCATION", os.path.join(BASE_DIR, ".ssh"))
SSH_KEYPAIR_NAME = env.str("SSH_KEYPAIR_NAME", default="id_rsa")

# Celery

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
