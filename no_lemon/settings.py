"""
Django settings for no_lemon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n_ynsu$)ru=zk06&3bm2uyas7$--&!s$xpnkpaq3u*ix&y==69'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['nolemon.antyc.ca']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inspections',
    'stripe',
    'bootstrap3_datetime',
    # 'mod_wsgi.server',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'no_lemon.urls'

WSGI_APPLICATION = 'no_lemon.wsgi.application'

AUTH_USER_MODEL = "inspections.BaseUser"

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_URL = '/register/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'America/Edmonton'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
    os.path.join(BASE_DIR, "documentation")
)

# site admins
ADMINS = (('Tyler', 'tyler.antyc@gmail.com'),
          ('Andrew', 'and.555@gmail.com'))

# email settings
EMAIL_USE_TLS = True
# prod, works in dev too
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
# dev
# run "python -m smtpd -n -c DebuggingServer localhost:1025" first
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025
EMAIL_HOST_USER = 'testnolemon'
EMAIL_HOST_PASSWORD = 'test1'

EMAIL_SUBJECT_PREFIX = '[NoLemon]'

# media
# prod
# MEDIA_ROOT = ''
# dev
MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

# constants
# these are in cents
INSPECTION_REQUEST = 10000
VIEW_INSPECTION_CHARGE_LVL_1 = 2999
VIEW_INSPECTION_CHARGE_LVL_2 = 3700
VIEW_INSPECTION_CHARGE_LVL_3 = 5600

# Stripe keys
STRIPE_KEY = 'pk_test_3aCn8J9IdHtqTUaCMWrABmQI'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

if os.path.isfile("../../test"):
    from configs.test_settings import *
elif os.path.isfile("../../prod"):
    from configs.prod_settings import *
elif os.path.isfile("../../devl"):
    pass  # Use settings.py as devl
else:
    raise Exception("There is no settings decision file.")
