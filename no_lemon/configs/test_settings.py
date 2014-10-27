# Test settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_HOSTS = ['nolemon.antyc.ca']

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

EMAIL_SUBJECT_PREFIX = '[NoLemon - Test]'
