"""
Django settings for facilis project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Unable debug in production
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'storage.db'),
    }
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
SECRET_KEY = '#h-w*c-hkmpikw5da24t_stu0!+(anl7zj$@=aj412&5_z8_q2'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'facilis.urls'
WSGI_APPLICATION = 'facilis.wsgi.application'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'suit',
    'django.contrib.admin',
    'south',
    'sap',
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    #('assets', os.path.join(BASE_DIR, 'static')),
    ('assets', os.path.join(BASE_DIR, 'media')),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Facilis',
    'HEADER_DATE_FORMAT': 'l, j \d\e F \d\e Y',

    # menu
    'SEARCH_URL': '',

    # misc
    'LIST_PER_PAGE': 15
}
