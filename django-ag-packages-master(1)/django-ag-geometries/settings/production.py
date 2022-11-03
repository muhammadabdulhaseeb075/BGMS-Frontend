
from .defaults import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    # '.bgms.co.uk',
    # '127.0.0.1',
    '.burialgrounds.co.uk'
]

CSRF_COOKIE_DOMAIN = '.burialgrounds.co.uk'

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
        'USER': 'django_admin',
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': 'dbdemo.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# # settings for s3 storage
# AWS_STORAGE_BUCKET_NAME = 'bgms'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

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
            'filename': '/home/BGMSproject/logging/django_debug.log',
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
AWS_STORAGE_BUCKET_NAME = 'bgms'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'config.storages.staticS3storage.StaticS3Storage'


# Django Compressor Settings
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
# COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
# COMPRESS_URL = STATIC_URL
# COMPRESS_STORAGE = STATICFILES_STORAGE
# COMPRESS_ROOT =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static_compressed')
# COMPRESS_JS_FILTERS = ['config.compressor.filters.UglifyFilter']
# COMPRESS_UGLIFYJS_ARGUMENTS = '--compress drop_debugger,drop_console'

# media files bucket
AWS_MEDIA_BUCKET_NAME = 'bgmsmedia'

# Email configurations
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'bgms@burialgrounds.co.uk'
EMAIL_AG_ADMIN = ['thurst@atlanticgeomatics.co.uk']

#Google Analytics
GOOGLE_ANALYTICS_KEY = 'UA-91162126-1'