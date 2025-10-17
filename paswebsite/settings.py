import os
from pathlib import Path
import environ
import dj_database_url


# -------------------------------------------------
# Initialize environment variables
# -------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False)
)

# Load environment variables from .env (for local dev)
environ.Env.read_env(BASE_DIR := Path(__file__).resolve().parent.parent / ".env")


# -------------------------------------------------
# Basic Project Settings
# -------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["pas.com.ng", "www.pas.com.ng", "localhost"]

# -------------------------------------------------
# Installed Apps
# -------------------------------------------------
INSTALLED_APPS = [
    # Cloudinary skipped intentionally (not used)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
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

# -------------------------------------------------
# Middleware
# -------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------
# URL & WSGI Configuration
# -------------------------------------------------
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

# -------------------------------------------------
# Database
# -------------------------------------------------
# ✅ SQLite locally, PostgreSQL on Render
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            default=env("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }

# -------------------------------------------------
# Password Validators
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------
# Internationalization
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Static & Media Files
# -------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------
# Crispy Forms
# -------------------------------------------------
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# -------------------------------------------------
# Authentication
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"

# -------------------------------------------------
# Paystack Configuration
# -------------------------------------------------
PAYSTACK_LIVE_SECRET_KEY = env("PAYSTACK_LIVE_SECRET_KEY")
PAYSTACK_LIVE_PUBLIC_KEY = env("PAYSTACK_LIVE_PUBLIC_KEY")
PAYSTACK_INITIALIZE_PAYMENT_URL = env("PAYSTACK_INITIALIZE_PAYMENT_URL")
PAYSTACK_VERIFY_URL = env("PAYSTACK_VERIFY_URL")

# -------------------------------------------------
# Email Configuration
# -------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.pas.com.ng"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "noreply@pas.com.ng"
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "noreply@pas.com.ng"

# -------------------------------------------------
# CSRF Trusted Origins
# -------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://www.pas.com.ng",
    "https://pas.com.ng",
]

# -------------------------------------------------
# Celery (optional)
# -------------------------------------------------
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# -------------------------------------------------
# Security Settings (Active in Production)
# -------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
