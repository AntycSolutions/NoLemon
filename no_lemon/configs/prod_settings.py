# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#Change
ALLOWED_HOSTS = ['nolemon.antyc.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_SUBJECT_PREFIX = '[NoLemon]'

#Change
STRIPE_KEY = 'pk_test_3aCn8J9IdHtqTUaCMWrABmQI'
