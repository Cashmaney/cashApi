from settings.common import *

print('Initializing prod configuration - \n')
PRODUCTION = True
print('PRODUCTION - %s\n'% PRODUCTION)
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
print('Debug - %s\n'% DEBUG)
'''
The following comes from:
http://rickchristianson.wordpress.com/2013/10/31/getting-a-django-app-to-use-https-on-aws-elastic-beanstalk/
'''
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

'''
The following comes from:
http://security.stackexchange.com/questions/8964/trying-to-make-a-django-based-site-use-https-only-not-sure-if-its-secure/8970#comment80472_8970
'''
#os.environ['HTTPS'] = "on"

ALLOWED_HOSTS=['*' ]

DATABASES = {
         'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         #'ENGINE': 'django.db.backends.mysql',
         'NAME': os.environ['RDS_DB_NAME'],
         'USER': os.environ['RDS_USERNAME'],
         'PASSWORD': os.environ['RDS_PASSWORD'],
         'HOST': os.environ['RDS_HOSTNAME'],
         'PORT': os.environ['RDS_PORT'],
         }
}
print('Database - %s\n' % DATABASES.get('NAME'))
# BOTO and django-storages
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'
STATIC_DIRECTORY = 'static/'  

#STATIC_URL = S3_STATIC_URL + STATIC_DIRECTORY

# https://github.com/ottoyiu/django-cors-headers/
# INSTALLED_APPS += ('corsheaders',)
# MIDDLEWARE_CLASSES = ('corsheaders.middleware.CorsMiddleware',) + MIDDLEWARE_CLASSES
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_URLS_REGEX = r'^/api.*$'
#CORS_ORIGIN_WHITELIST = ('*',)

print('End of settings file')
