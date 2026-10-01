from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure parent directory is in sys.path so django_daisy_theme is found directly
sys.path.insert(0, str(BASE_DIR.parent))

SECRET_KEY = "django-insecure-demo-secret-key-for-daisy-theme-testing"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django_daisy_theme",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo.urls"

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
                "django_daisy_theme.context_processors.daisy_theme_context",
            ],
        },
    },
]

WSGI_APPLICATION = "demo.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

# Localization & RTL setup
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("fa", "فارسی"),
    ("en", "English"),
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Daisy Theme Configuration
DAISY_THEME_CONFIG = {
    "SITE_TITLE": "پنل مدیریت فروشگاه مدرن",
    "SITE_HEADER": "فروشگاه دیزی",
    "SITE_LOGO": "/static/django_daisy_theme/img/logo.svg",
    "DEFAULT_THEME": "light",
    "DARK_THEME": "dark",
    "SHOW_THEME_SWITCHER": True,
    "AVAILABLE_THEMES": [
        "light",
        "dark",
        "emerald",
        "cupcake",
        "corporate",
        "synthwave",
        "night",
    ],
    "DIRECTION": "auto",
    "LOAD_DEFAULT_FONTS": True,
    "COLLAPSIBLE_SIDEBAR": True,
    "SHOW_RECENT_ACTIONS": True,
    "CUSTOM_LINKS": [
        {
            "title": "گیت‌هاب پروژه",
            "url": "https://github.com",
            "icon": "globe",
            "target": "_blank",
        },
    ],
    "FOOTER_TEXT": "طراحی شده با عشق توسط django-daisy-theme",
    "SHOW_VERSION": True,
}
