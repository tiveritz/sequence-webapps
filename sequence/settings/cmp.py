import os

import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment Variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, './.env'))


SECRET_KEY = env('SECRET_KEY', default='')
DEBUG = env.bool('DEBUG', default=False)
SECURE_SSL_REDIRECT = False
AJAX_SCHEME = env('AJAX_SCHEME', default='https')

MAILJET_API_KEY = env('MAILJET_API_KEY', default='')
MAILJET_API_SECRET = env('MAILJET_API_SECRET', default='')

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', default='')
GOOGLE_MAPS_ID = os.getenv('GOOGLE_MAPS_ID', default='')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'django_countries',

    # Own
    'website',
    'backend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Language detection:
    # Should always come before CommonMiddleware and after Session Middleware
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # i18n url patterns
    'django.middleware.locale.LocaleMiddleware',
    # www to non-www redirect
    'hausstefan.middleware.WwwRedirectMiddleware',
]

ROOT_URLCONF = 'hausstefan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hausstefan.wsgi.application'


# Database
DATABASES = {
    'default': env.db('DATABASE', default='postgresql://')
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('de', 'German'),
    ('en', 'English'),
]

TIME_ZONE = 'Europe/Vienna'
DATE_FORMAT = '%d.%m.%Y'

USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'hausstefan/locale'),
    os.path.join(BASE_DIR, 'website/locale'),
    os.path.join(BASE_DIR, 'mailjet/locale'),
]


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication
LOGIN_REDIRECT_URL = 'backend'
LOGOUT_REDIRECT_URL = '/'
