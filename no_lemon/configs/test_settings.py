# Test settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_HOSTS = ['nolemon.antyc.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nolemon',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

EMAIL_SUBJECT_PREFIX = '[NoLemon - Test]'
