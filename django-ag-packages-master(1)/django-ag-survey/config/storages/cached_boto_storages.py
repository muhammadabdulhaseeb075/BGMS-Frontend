from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from django.conf import settings
from uuid import uuid4
import os
from django.contrib.staticfiles.storage import ManifestFilesMixin,\
    CachedFilesMixin, CachedStaticFilesStorage

#DeprecationWarning from version > v0.4.11
class CachedS3BotoStorage(CachedFilesMixin, S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too. For use of staticfiles app.
    """
    def __init__(self, *args, **kwargs):
        super(CachedFilesMixin, self).__init__(*args, **kwargs)
        super(S3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
#         if settings.COMPRESS_OUTPUT_DIR in name:
#             # setting a unique hash id for each compressed file during each compression
#             name = os.path.join(settings.COMPRESS_OUTPUT_DIR, str(uuid4()).join(name.split(settings.COMPRESS_OUTPUT_DIR)))
#         name = super(CachedStaticFilesStorage, self).save(name, content)
        name = super(S3BotoStorage, self).save(name, content)
        super(S3BotoStorage, self).save(self.hashed_name(name, content), content)
        self.local_storage._save(name, content)
        self.local_storage._save(self.hashed_name(name, content), content)
        return name

    def url_hashed(self, name):
        try:
            hashed_name = self.hashed_name(name)
            if self.exists(hashed_name):
                return super(CachedS3BotoStorage, self).url(hashed_name)
            else:
                return super(CachedS3BotoStorage, self).url(name)
        except:
            return super(CachedS3BotoStorage, self).url(name)
# FIN DeprecationWarning


