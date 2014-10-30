# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_HOSTS = ['nolemon.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nolemon',
        'USER': 'django',
        'PASSWORD': 'proddjangopostgresql',
        'HOST': 'localhost'
    }
}

EMAIL_SUBJECT_PREFIX = '[NoLemon]'

#Change
STRIPE_KEY = 'pk_test_3aCn8J9IdHtqTUaCMWrABmQI'
