
from .defaults import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    # '.bgms.co.uk',
    # '127.0.0.1',
    '.burialgrounds.co.uk'
]

DATABASES = {
    # 'default': {
    #     'ENGINE': 'config.db.backends.postgres',
    #     'NAME': 'BGMS_DB',
    #     'USER': 'django_dev',
    #     'PASSWORD': '7204$BGM$AG',
    #     'HOST': 'devdbinstance.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
    #     'PORT': '5432',
    # }
    'default': {
        'ENGINE': 'config.db.backends.postgres',
        'NAME': 'BGMS_DB',
        'USER': 'bgms_admin',
        'PASSWORD': 'AG$7204$BGMS',
        'HOST': 'dbdemo.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}



# settings for compressed s3 storage
AWS_STORAGE_BUCKET_NAME = 'bgmscompressed'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
