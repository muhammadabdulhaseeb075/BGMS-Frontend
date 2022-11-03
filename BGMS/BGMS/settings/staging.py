from .defaults import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STAGING_PORT = 81
HOMEPAGE = 'https://burialgrounds.co.uk:' + str(STAGING_PORT)

ALLOWED_HOSTS = [
    # '.bgms.co.uk',
    # '127.0.0.1',
    '.burialgrounds.co.uk'
]

CORS_ORIGIN_WHITELIST = [
    "https://burialgrounds.co.uk:" + str(STAGING_PORT),
]

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_DOMAIN = '.burialgrounds.co.uk'

CSRF_COOKIE_DOMAIN = 'burialgrounds.co.uk:' + str(STAGING_PORT)

ORIGINAL_BACKEND = "django.contrib.gis.db.backends.postgis"

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
       'ENGINE': 'tenant_schemas.postgresql_backend',
       'NAME': 'BGMS_STAGING',
       'USER': 'django_admin',
       'PASSWORD': os.environ.get('DB_PASSWORD', ''),
       'HOST': 'dbdemo.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
       'PORT': '5432',
    } #End Staging db - now running v13
    # 'default': {
    #     'ENGINE': 'tenant_schemas.postgresql_backend',
    #     'NAME': 'BGMS_STAGING',
    #     'USER': 'django_admin',
    #     'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    #     'HOST': 'dbdemo-2021-11-16.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
    #     'PORT': '5432',
    # }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/BGMSstaging/logging/django_debug.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# settings for compressed s3 storage
AWS_STORAGE_BUCKET_NAME = 'bgmscompressed'
# reverting back to s3 from cloudfront
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_CUSTOM_DOMAIN = '%s.burialgrounds.co.uk' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'config.storages.staticS3storage.StaticS3Storage'

# media files bucket
AWS_MEDIA_BUCKET_NAME = 'bgmsmedia'


# Email configurations
EMAIL_AG_ADMIN = ['psimpson@atlanticgeomatics.co.uk']

#Google Analytics
GOOGLE_ANALYTICS_KEY = 'UA-91162126-1'