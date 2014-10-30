# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_HOSTS = ['nolemon.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nolemon',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

EMAIL_SUBJECT_PREFIX = '[NoLemon]'

#Change
STRIPE_KEY = ''
