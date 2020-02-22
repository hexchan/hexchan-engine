import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

# Paths
SETTINGS_PATH = Path(__file__).resolve()
BASE_DIR = SETTINGS_PATH.parents[1]
INSTALL_DIR = BASE_DIR.parent
STORAGE_DIR = INSTALL_DIR / 'storage'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cl-x4wji(%=&43=*tla3+n-)vr4220%(_tiwh&@^(=dyw*=r2x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts
HOST = 'example.com'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', HOST]
INTERNAL_IPS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'imageboard',
    'captcha',
    'moderation',

    # Third party
    'debug_toolbar',
]

# Middleware
MIDDLEWARE = [
    # Third party
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'hexchan.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Django processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

                # App processors
                'imageboard.context_processors.config',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'hexchan.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hexchan',
        'USER': 'hexchan',
        'PASSWORD': 'swordfish',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and time
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
  ('ru', _('Russian')),
  ('en', _('English')),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = str(STORAGE_DIR / 'static')
STATICFILES_DIRS = []

# Uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = str(STORAGE_DIR / 'upload')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': str(STORAGE_DIR / 'cache'),
    #     'TIMEOUT': 60 * 60,  # 1 hour
    #     'OPTIONS': {
    #         'MAX_ENTRIES': 10000
    #     }
    # },
}

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = str(STORAGE_DIR / 'session')
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days in seconds

# Generated fixtures
FIXTURE_DIRS = [
    str(STORAGE_DIR / 'fixtures')
]
