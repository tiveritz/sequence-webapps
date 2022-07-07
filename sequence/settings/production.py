from sequence.settings.base import *

# Static files
ADMIN_MEDIA_PREFIX = '/static/cms/'
STATIC_ROOT = '/data/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_REDIRECT_URL = '/cms/dashboard/'
LOGOUT_REDIRECT_URL = '/cms/'


#Storage Bucket
AWS_STORAGE_BUCKET_NAME = 'tiverspace'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'

STATICFILES_LOCATION = 'sequence/webapps/static/'
STATICFILES_STORAGE = 'sequence.storages.StaticRootS3Boto3Storage'
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'sequence/webapps/media/'
DEFAULT_FILE_STORAGE = 'sequence.storages.MediaRootS3Boto3Storage'
MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, MEDIAFILES_LOCATION)
