# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

#Change
ALLOWED_HOSTS = ['nolemon.antyc.ca']

#Change
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nolemon',
        'USER': 'django',
        'PASSWORD': 'testdjangomysql',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_SUBJECT_PREFIX = '[NoLemon]'

#Change
STRIPE_KEY = 'pk_test_3aCn8J9IdHtqTUaCMWrABmQI'
