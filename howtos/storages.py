from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'howtos/webapp/static'

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'howtos/webapp/media'
