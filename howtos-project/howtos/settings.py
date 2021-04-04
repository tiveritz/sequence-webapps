from pathlib import Path
import os
from dotenv import load_dotenv

# Prepare environment variables
def parse_env_boolean(variable_name):
    var = os.getenv(variable_name).lower()

    if (var == 'true'): return True
    if (var == 'false'): return False
    raise AttributeError('Environment variable does not equal to either true or false')


load_dotenv()

ENV_DEBUG = parse_env_boolean('DEBUG')
ENV_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
ENV_SECURE_SSL_REDIRECT = parse_env_boolean('SECURE_SSL_REDIRECT')
ENV_DB_NAME = os.getenv('DB_NAME')
ENV_DB_USER = os.getenv('DB_USER')
ENV_DB_PASS = os.getenv('DB_PASS')
ENV_DB_HOST = os.getenv('DB_HOST')
ENV_SECRET_KEY = os.getenv('SECRET_KEY')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_DEBUG

ALLOWED_HOSTS = ENV_ALLOWED_HOSTS

SECURE_SSL_REDIRECT = ENV_SECURE_SSL_REDIRECT

    
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'administration',
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

ROOT_URLCONF = 'howtos.urls'

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

WSGI_APPLICATION = 'howtos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV_DB_NAME,
        'USER': ENV_DB_USER,
        'PASSWORD': ENV_DB_PASS,
        'HOST': ENV_DB_HOST,
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'd.m.Y H:i'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Static files
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = '/home/ht.tiveritz.at/public_html/howtos-project/public/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
