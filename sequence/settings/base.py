import os

import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment Variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, './.env'))


SECRET_KEY = env('SECRET_KEY', default='')
DEBUG = env.bool('DEBUG', default=False)
#AJAX_SCHEME = env('AJAX_SCHEME', default='https')

VERSION = os.getenv('VERSION')


#
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
REQUESTS_SSL_VERIFICATION = env.bool('REQUESTS_SSL_VERIFICATION', True)

API_URL = os.getenv('API_URL')

    
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'storages',
    
    # Own
    'cms',
    'project',
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

ROOT_URLCONF = 'sequence.urls'

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

        'libraries':{
            'pagination': 'cms.templatetags.pagination',
            
            }
        },
    },
]

WSGI_APPLICATION = 'sequence.wsgi.application'


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

TIME_ZONE = 'Europe/Vienna'
DATE_FORMAT = '%d.%m.%Y'

USE_I18N = True
USE_TZ = True
