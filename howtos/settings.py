from pathlib import Path
import os
from dotenv import load_dotenv

# Prepare environment variables
def parse_env_boolean(variable_name):
    if not os.getenv(variable_name):
        raise ImportError(f'Variable name "{variable_name}" not found in .env')

    var = os.getenv(variable_name).lower()

    if (var == 'true'): return True
    if (var == 'false'): return False
    raise AttributeError('Environment variable does not equal to either true or false')


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = parse_env_boolean('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

SECURE_SSL_REDIRECT = parse_env_boolean('SECURE_SSL_REDIRECT')

REQUESTS_SSL_VERIFICATION = parse_env_boolean('REQUESTS_SSL_VERIFICATION')

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
    'storages',
    
    # Own
    'administration',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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
#STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = '/data/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_REDIRECT_URL = '/administration/dashboard/'
LOGOUT_REDIRECT_URL = '/administration/'

# Storage Bucket
'''
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'tiverspace'
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'

DEFAULT_FILE_STORAGE = 'howtos.storages.MediaRootS3Boto3Storage'
STATICFILES_STORAGE = 'howtos.storages.StaticRootS3Boto3Storage'

STATIC_URL = 'https://tiverspace.fra1.digitaloceanspaces.com/howtos/webapps/static/'
'''


#Storage Bucket
AWS_STORAGE_BUCKET_NAME = 'tiverspace'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'

STATICFILES_LOCATION = 'howtos/webapps/static/'
STATICFILES_STORAGE = 'howtos.storages.StaticRootS3Boto3Storage'
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'howtos/webapps/media/'
DEFAULT_FILE_STORAGE = 'howtos.storages.MediaRootS3Boto3Storage'
MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, MEDIAFILES_LOCATION)