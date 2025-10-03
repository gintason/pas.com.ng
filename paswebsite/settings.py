import os
from pathlib import Path
import environ  # <--- add this
# at top of settings.py
import pymysql


# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

pymysql.install_as_MySQLdb()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / ".env")

# Security
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")

# Allowed hosts
ALLOWED_HOSTS = ["pas.com.ng", "www.pas.com.ng", 'localhost']

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pasApp",
    "users",
    "crispy_forms",
    "bootstrap5",
    "Blog",
    "payments",
    "widget_tweaks",
    "quiz",
    "crispy_bootstrap5",
    "untimed_quiz",
    "import_export",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "paswebsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "paswebsite.wsgi.application"


# ✅ Database: SQLite locally, MySQL on Render
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT", default="3306"),
        }
    }


# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# Authentication
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"

# Paystack
PAYSTACK_LIVE_SECRET_KEY = env("PAYSTACK_LIVE_SECRET_KEY")
PAYSTACK_LIVE_PUBLIC_KEY = env("PAYSTACK_LIVE_PUBLIC_KEY")
PAYSTACK_INITIALIZE_PAYMENT_URL = env("PAYSTACK_INITIALIZE_PAYMENT_URL")
PAYSTACK_VERIFY_URL = env("PAYSTACK_VERIFY_URL")

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.pas.com.ng"     # Outgoing SMTP
EMAIL_PORT = 465                   # Use SSL
EMAIL_USE_TLS = False              # ❌ Not TLS
EMAIL_USE_SSL = True               # ✅ SSL on port 465
EMAIL_HOST_USER = "noreply@pas.com.ng"
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "noreply@pas.com.ng"

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://www.pas.com.ng",
    "https://pas.com.ng",
]

# Celery
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Security (only active in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
