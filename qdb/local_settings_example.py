import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ENVIRONMENT = os.path.split(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
)))[1]

ALLOWED_HOSTS = ['qdb.invalid']

ADMINS = (('Admin', 'admin@qdb.invalid'),)

TIME_ZONE = 'America/Chicago'
USE_TZ = True

DATABASES = {
    # Refer to https://docs.djangoproject.com/en/dev/ref/settings/#databases
}

# Make this unique
SECRET_KEY = ''

BASE_URL = 'http://qdb.invalid/'

QDB_NAME = 'My QDB'
