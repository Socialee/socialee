from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class S3StaticStorage(S3BotoStorage):
    "S3 storage backend that sets the static bucket."
    def __init__(self, *args, **kwargs):
        super(S3StaticStorage, self).__init__(bucket=settings.AWS_STATIC_BUCKET_NAME, *args, **kwargs)