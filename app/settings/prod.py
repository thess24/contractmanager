"""Production settings and globals."""


from os import environ
# from memcacheify import memcacheify
from postgresify import postgresify
from S3 import CallingFormat

from common import *


DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
# TEMPLATE_DEBUG = DEBUG
 

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"


# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
# EMAIL_USE_TLS = True

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
# EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.mandrillapp.com')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
# EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
# EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
# EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
# EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
# SERVER_EMAIL = EMAIL_HOST_USER

# DEFAULT_FROM_EMAIL = environ.get('EMAIL_HOST_USER', '')  #for use with windows live 
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': environ['RDS_DB_NAME'],
		'USER': environ['RDS_USERNAME'],
		'PASSWORD': environ['RDS_PASSWORD'],
		'HOST': environ['RDS_HOSTNAME'],
		'PORT': environ['RDS_PORT'],
	}
}

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = memcacheify()
########## END CACHE CONFIGURATION


########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
    # 'djrill'
)

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# had to do this to get a3 to serve static and media
DEFAULT_FILE_STORAGE = 'app.settings.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'app.settings.s3utils.StaticRootS3BotoStorage'

# # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

# # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# # AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY,
        AWS_EXPIRY)
}

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
S3_URL = 'https://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + '/static/'
MEDIA_URL = S3_URL + '/media/'

# COMPRESS_URL = STATIC_URL 
########## END STORAGE CONFIGURATION



########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
########## END SECRET CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', '.elasticbeanstalk.com', '.baldurhealthcare.com']
########## END ALLOWED HOST CONFIGURATION




############ ALL AUTH

# ACCOUNT_EMAIL_VERIFICATION='mandatory'



############ SSL

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

## ssl will not work if debug=True
## https://github.com/rdegges/django-sslify



####### DJRILL - MANDRILL EMAIL

# MANDRILL_API_KEY = environ.get('MANDRILL_API_KEY', "")


