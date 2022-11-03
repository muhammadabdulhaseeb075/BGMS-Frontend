from .defaults import *

INTERNAL_IPS = (
    '.bgms.com',
    '0.0.0.0',
    '127.0.0.1',
    '.localhost',
    'adlington.burialgrounds.co.uk',
'abbotsbromley.burialgrounds.co.uk',
'burialgrounds.co.uk',
'caldbeckdemo.burialgrounds.co.uk',
    'handsworthmary.bgms.com',
    'brandwoodend2.bgms.com',
    'western.bgms.com',
    'adlington.bgms.com',
    'staines.bgms.com',
    'highgate.bgms.com',
    'bramham.bgms.com',
    'pershore.bgms.com',
    'apperknowle.bgms.com',
    'warstone.bgms.com',
    'burialgrounds.co.uk',
    '192.168.17.114',
    '192.168.2.40',
    '192.168.2.28'
)

DEBUG = True

# ALLOWED_HOSTS = [
#     '.bgms.com',
#     '127.0.0.1',
#     '.localhost',    
#     'adlington.burialgrounds.co.uk',
#     'abbotsbromley.burialgrounds.co.uk',
#     'handsworthmary.burialgrounds.co.uk',
#     'brandwoodend2.burialgrounds.co.uk',
#     'western.burialgrounds.co.uk',
#     'staines.burialgrounds.co.uk',
#     'highgate.burialgrounds.co.uk',
#     'burialgrounds.co.uk',
#     '192.168.17.114',
#     '192.168.2.40',
#     '192.168.2.28',
#     'caldbeckdemo.burialgrounds.co.uk'
# ]
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = [
    "https://bgms.com:8000",
    "https://burialgrounds.co.uk:8000",
    "https://burialgrounds.co.uk",
    "https://caldbeckdemo.burialgrounds.co.uk:8000"
]

CORS_ALLOW_CREDENTIALS = True

HOMEPAGE = 'https://caldbeckdemo.burialgrounds.co.uk:8000'
#HOMEPAGE = 'https://burialgrounds.co.uk'

#SESSION_COOKIE_DOMAIN = '.bgms.com'
#SESSION_COOKIE_DOMAIN = '.burialgrounds.co.uk'

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_DOMAIN = None

ORIGINAL_BACKEND = "django.contrib.gis.db.backends.postgis"

DATABASES = {
        # 'default': {
        #     'ENGINE': 'config.db.backends.postgres',
        #     'NAME': 'BGMS_DB_D7',
        #     'USER': 'postgres',
        #     'PASSWORD': 'root',
        #     'HOST': 'localhost',
        #     'PORT': '5432',
        # }
    #'default': {
    #    'ENGINE': 'tenant_schemas.postgresql_backend',
    #    'NAME': 'BGMS_DEV2',
    #    'USER': 'postgres',
    #    'PASSWORD': 'password',
    #    'HOST': 'syddsql04.local',
    #    'PORT': '5432',
    #}
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'BGMS_DB',
        'USER': 'bgms_admin',
        'PASSWORD': 'AGbGm57204RdSmaster',
        'HOST': 'dbdemo.c2sriuehqiis.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }  
    # 'default': {
    #     'ENGINE': 'tenant_schemas.postgresql_backend',
    #     'NAME': 'BGMS_LOCAL',
    #     'USER': 'postgres',
    #     'PASSWORD': 'admin',
    #     'HOST': '',
    #     'PORT': '5432',
    # }

    
}

## Middleware for silk
#MIDDLEWARE += (
     #'silk.middleware.SilkyMiddleware',
     #'debug_toolbar.middleware.DebugToolbarMiddleware',     
     #'debug_panel.middleware.DebugPanelMiddleware',
#)

## Middleware for AppMap
MIDDLEWARE += (
    #'appmap.django.Middleware',    
)




# settings for debug toolbar and silk
INSTALLED_APPS += (
    'sslserver',
    #'debug_toolbar',
    #'silk',   
    #'debug_panel',     
)

#DEBUG_TOOLBAR_PATCH_SETTINGS = False

#DEBUG_TOOLBAR_PANELS = [
#    'ddt_request_history.panels.request_history.RequestHistoryPanel', #for ajax requests debug
#    'debug_toolbar.panels.versions.VersionsPanel',
#    'debug_toolbar.panels.timer.TimerPanel',
#    'debug_toolbar.panels.settings.SettingsPanel',
#    'debug_toolbar.panels.headers.HeadersPanel',
#    'debug_toolbar.panels.request.RequestPanel',
#    'debug_toolbar.panels.sql.SQLPanel',
#    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#    'debug_toolbar.panels.templates.TemplatesPanel',
#    'debug_toolbar.panels.cache.CachePanel',
#    'debug_toolbar.panels.signals.SignalsPanel',
#    'debug_toolbar.panels.logging.LoggingPanel',
#    'debug_toolbar.panels.redirects.RedirectsPanel',    
#]

#DEBUG_TOOLBAR_CONFIG = {
#    'SHOW_TOOLBAR_CALLBACK': 'ddt_request_history.panels.request_history.allow_ajax',
#    'RESULTS_CACHE_SIZE': 100,
#}

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
            'filename': 'C:\\BGMS\\BGMS-Scotia\\logs\\django_a.log',
            'formatter': 'verbose',
            'delay': True
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.django.security.*': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_FROM_S3 = False

if STATIC_FROM_S3:

    # settings for compressed s3 storage
    AWS_STORAGE_BUCKET_NAME = 'bgmsdevelopmentstatic'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'config.storages.staticS3storage.StaticS3Storage'
   #settings for compressed s3 storage
    # AWS_STORAGE_BUCKET_NAME = 'bgms36'
    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    # STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    # STATICFILES_STORAGE = 'config.storages.staticS3storage.StaticS3Storage'


    # import datetime

    # two_months = datetime.timedelta(days=61)
    # date_two_months_later = datetime.date.today() + two_months
    # expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

    # AWS_HEADERS = {
    #     'Expires': expires,
    #     'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
    # }

else:
    # COMPRESS_ENABLED = False
    STATIC_URL = '/static/'



GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

#settings for using modelmommy with geodjango

def mommy_multipolygon_field():
    from django.contrib.gis.geos import MultiPolygon, Polygon
    p1 = Polygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    return MultiPolygon(p1)

def mommy_multiline_field():
    from django.contrib.gis.geos import LineString, MultiLineString
    ls1 = LineString((0, 0), (1, 1))
    return MultiLineString(ls1)

def mommy_point_field():
    from django.contrib.gis.geos import Point
    return Point(0, 0)

MOMMY_CUSTOM_FIELDS_GEN = {
    'django.contrib.gis.db.models.fields.MultiPolygonField': mommy_multipolygon_field,
#     'django.contrib.gis.db.models.fields.MultiLineString': mommy_multiline_field,
#     'django.contrib.gis.db.models.fields.Point': mommy_point_field,
}

# media files bucket
#AWS_MEDIA_BUCKET_NAME = 'bgmsmedia-dev'
AWS_MEDIA_BUCKET_NAME = 'bgmsmedia'

#MEDIA_URL = 'C:/media/'
#MEDIA_ROOT = 'C:/media/'

# Email configurations
EMAIL_AG_ADMIN = ['psimpson@atlanticgeomatics.co.uk']

#Protocol redirect http for local development
PROTOCOL_REDIRECT = 'http://'

#Google Analytics
# GOOGLE_ANALYTICS_KEY = 'UA-91162126-1'
GOOGLE_ANALYTICS_KEY = ''

#Temporary folder to process uploaded files
TEMP_FILES_UPLOAD_PATH = '/Users/troy/Projects/BGMS/temp/'

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/javascript", ".js", True)