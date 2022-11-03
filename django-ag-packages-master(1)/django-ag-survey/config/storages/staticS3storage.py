
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
 
class StaticS3Storage(ManifestFilesMixin, S3BotoStorage):
    pass


StaticRootS3BotoStorage = lambda: S3BotoStorage(bucket_name=settings.AWS_STORAGE_BUCKET_NAME)
# MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')



class StaticShareS3Storage(S3BotoStorage):
    bucket_name=settings.AWS_STORAGE_BUCKET_NAME_SHARED
    # custom_domain=setting.AWS_S3_CUSTOM_DOMAIN_SHARED
    file_overwrite = False
    custom_domain = None

    # def url(self, *a, **kw):
    #     s = super(StaticShareS3Storage, self).url(*a, **kw)
    #     # s = urllib.parse.quote_plus(s.strip())
    #     # o = urlparse(s)
    #     # return urllib.parse.quote_plus(s)
    #     return s.replace('+','%2B')
