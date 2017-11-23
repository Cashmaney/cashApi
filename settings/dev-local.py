from settings.common import *

print('Initializing debug configuartion - ')

PRODUCTION = False
print('PRODUCTION - %s\n' % PRODUCTION)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
print('Debug - %s\n' % DEBUG)

ALLOWED_HOSTS=['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
}
print('Database - %s\n' % DATABASES.get('NAME'))
print('End of settings file')

