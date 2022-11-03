"""
Django settings for BGMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = '5656'

#session settings
#SECURITY WARNING: change to true once we have an ssl certificate
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#fix to resolve csrf verification failing on IE
CSRF_COOKIE_NAME = 'xcsrfcookie'
CSRF_COOKIE_AGE = None
CSRF_COOKIE_HTTPONLY = True

# Application definition

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    # 'debug_panel.middleware.DebugPanelMiddleware',
]

ROOT_URLCONF = 'BGMS.urls'

PUBLIC_SCHEMA_URLCONF = 'BGMS.public_urls'

WSGI_APPLICATION = 'BGMS.wsgi.application'

AUTH_USER_MODEL = 'main.BGUser'

AUTHENTICATION_BACKENDS = ('config.auth.backends.TenantModelBackend',)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# TODO: caches - replace with memcached later
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#         'TIMEOUT': 300
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'BGMS','templates'),
            os.path.join(BASE_DIR, 'mapmanagement','templates'),
            os.path.join(BASE_DIR, 'datamatching','templates'),
            os.path.join(BASE_DIR, 'dataentry','templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
            ],
        },
    },
]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
# LOGOUT_URL

# django-tenant-squema

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

SHARED_APPS = (

    'surveypublic',
    'django.contrib.contenttypes',
)

TENANT_APPS = (
    # your tenant-specific apps

    'survey',
    'geometries',
#     removed 'django.contrib.auth' from here because if auth tables are created in the tenant,
#     it is not secure because our sessions for authorised users are in main
)

TENANT_MODEL = "main.burialgroundsite" # app.Model

# PUBLIC_SCHEMA_NAME = "bgms_public"

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(os.path.dirname(__file__),BASE_DIR,),
    #Angular JS app for each Django app
    os.path.join(BASE_DIR,'mapmanagement','static'),
    os.path.join(BASE_DIR,'datamatching','static'),
    os.path.join(BASE_DIR,'dataentry','static'),
    #to use of share assets and libs
    os.path.join(BASE_DIR,'BGMS','static'),
    os.path.join(BASE_DIR,'main','static'),
)

# STATIC_ROOT = os.path.join(BASE_DIR,'BGMS','build')

# settings for tenant-specific s3 media storage
DEFAULT_FILE_STORAGE = 'config.storages.media_storages.TenantMediaStorage'

# settings for tenant-specific s3 media storage end

# Static files (CSS, JavaScript, Images)
# settings for s3 storage
# AWS Access key and secret access key used by DEFAULT_FILE_STORAGE as well as STATICFILES_STORAGE
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# settings for s3 end

# Deprecated from version > v0.4.11
COMPRESS_ROOT =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static_compressed')
# Deprecated from version > v0.4.11

#File uploads settings
CONTENT_TYPES = ['image']
FILE_TYPES = ['png', 'jpeg', 'jpg']
# MAX_UPLOAD_SIZE = 5242880
MAX_UPLOAD_SIZE = 99999999999999999

# Deprecated from version > v0.4.11
#Sass Compiler
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    # ('text/x-scss', 'sassc {infile} {outfile}'), #to compile with SassC wrapper around libsass (c++)
)
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']
# Deprecated from version > v0.4.11

#Temporary folder to process uploaded files
TEMP_FILES_UPLOAD_PATH = '/bgmstemp/'


"""
Map creation, base and aerial layers
"""
RESOLUTIONS = '[2800.0, 1400.0, 700.0, 350.0, 280, 140, 70, 28.0, 14.0, 7.0, 2.8, 1.4,0.7, 0.28, 0.14, 0.07, 0.028]'
MATRIXIDS = '[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]'
"""
FIN: Map creation, base and aerial layers
"""

# media files bucket structure
AWS_MEDIA_BUCKET_NAME_STRUCTURE = ['/images/burial_records/','/images/memorials/', '/images/user_uploads/',
                                    '/thumbnails/burial_records/','/thumbnails/memorials/', '/thumbnails/user_uploads/',
                                    '/files/']

# static share bucket across schemas with signature
AWS_STORAGE_BUCKET_NAME_SHARED = 'bgmssign'
AWS_S3_CUSTOM_DOMAIN_SHARED = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME_SHARED

CSRF_FAILURE_VIEW = 'config.security.views.csrf_failure'

#Protocol redirect (Default https for staging and production)
PROTOCOL_REDIRECT = 'https://'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


