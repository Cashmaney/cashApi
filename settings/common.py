"""
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from cashApi.apps import AppConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_PROJECT_DIR = os.path.join(BASE_DIR, 'services')
print('BASE_PROJECT_DIR = %s' % BASE_PROJECT_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v*kswpdyi3+*-=q4a)7&_!xwb%@udm1vi56r690!!j6e*p3^mn'

ALLOWED_HOSTS = ['myapp.com', 'localhost', '10.0.0.9', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'cashApi.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework_social_oauth2',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MEDIA_ROOT = os.path.join(BASE_PROJECT_DIR, 'Storage')
print('MEDIA_ROOT = %s' % MEDIA_ROOT)

ROOT_URLCONF = 'cashApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'cashApi.wsgi.application'

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GooglePlusAuth',
    'social_core.backends.email.EmailAuth',
    'social_core.backends.username.UsernameAuth',
    'social_core.backends.upwork.UpworkOAuth',
    'social_core.backends.slack.SlackOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

# config per http://psa.matiasaguirre.net/docs/configuration/django.html#django-admin
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

# If this is not set, PSA constructs a plausible username from the first portion of the
# user email, plus some random disambiguation characters if necessary.
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '754062895050-aivtptb5vttbqjtcl9vblta489oificg.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY_AUD = '754062895050-aivtptb5vttbqjtcl9vblta489oificg.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'AIzaSyA1paLrcvfdUzHhJY_K67SRAOmeZsJAYeA'

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile'
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'common.pipeline.require_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.debug.debug',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.debug.debug'
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db1',
#         'USER': 'root',
#         'PASSWORD': '1',
#         'HOST': 'aaplt5iga3iws2.cjzllicaijms.eu-central-1.rds.amazonaws.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             'read_default_file': '/etc/mysql/my.cnf',
#         },
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# try:
#     from example.local_settings import *
# except ImportError:
#     pass

DEBUG_LOG_DIR = BASE_DIR + "/django_debug.log"
# Django Logging

# one email per XX seconds
LOGLIMIT_RATE = 10

# uses keys to detect which errors are the same
LOGLIMIT_MAX_KEYS = 100

# uses cache if it's available
LOGLIMIT_CACHE_PREFIX = 'LOGLIMIT'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'null': {
            'level': 'ERROR',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

