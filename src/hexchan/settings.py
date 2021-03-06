# Standard libs
from pathlib import Path
from email.utils import getaddresses
from collections import OrderedDict

# Third party libs
from environ import Env

# Django libs
from django.utils.translation import gettext_lazy as _


# Base paths
SETTINGS_PATH = Path(__file__).resolve()
BASE_DIR = SETTINGS_PATH.parents[1]
INSTALL_DIR = BASE_DIR.parent

# Setup environment loader
env = Env(
    DEBUG=(bool, False),
    STORAGE_DIR=(str, None),
)

# Load .env file
with open(INSTALL_DIR / '.env', 'r') as env_config_file:
    Env.read_env(env_config_file)

# Storage directory
STORAGE_DIR = Path(env('STORAGE_DIR')) if env('STORAGE_DIR') else (INSTALL_DIR / 'storage')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Hosts
HOST = env('HOST', default='example.com')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', HOST]
INTERNAL_IPS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'constance',
    'constance.backends.database',
    'debug_toolbar',

    # Project apps
    'imageboard',
    'moderation',
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
                # Third party processors
                'constance.context_processors.config',

                # Django processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

                # App processors
                'imageboard.context_processors.admin_email',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'hexchan.wsgi.application'

# Database
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='sqlite:///{storage_dir}/hexchan.db'.format(storage_dir=STORAGE_DIR)
    ),
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
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en')
LANGUAGES = [
  ('ru', _('Russian')),
  ('en', _('English')),
]
TIME_ZONE = env('TIME_ZONE', default='UTC')
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

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = str(STORAGE_DIR / 'session')
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days in seconds

# Generated fixtures
FIXTURE_DIRS = [
    str(STORAGE_DIR / 'fixtures')
]

# Mail
EMAIL_CONFIG = env.email_url('EMAIL_URL', default='dummymail://')
vars().update(EMAIL_CONFIG)

# Admins
ADMINS = getaddresses([env('DJANGO_ADMINS', default='root@localhost')])

# Admin-editable constants
CONSTANCE_CONFIG = OrderedDict([
    (
        'SITE_NAME',
        (
            'Hexchan',
            _('Site title'),
        ),
    ),
    (
        'SITE_DESCRIPTION',
        (
            'Yet another anonymous imageboard',
            _('Site description, used in the main page\'s "description" meta tag content'),
        ),
    ),
    (
        'SITE_KEYWORDS',
        (
            'imageboard, anonymous, fun',
            _('Site keywords, used as the main page\'s "keywords" meta tag content'),
        ),
    ),
    (
        'MAIN_PAGE_WELCOMING_TEXT',
        (
            '#Hello world!',
            _('The welcoming text displayed on the main page (Markdown is supported)')
        ),
    ),
    (
        'LOGO_IMAGE',
        (
            '',
            _('Site logo, displayed in the site header'),
            'image_field'
        ),
    ),
    (
        'FAVICON',
        (
            '',
            _('Site favicon, displayed in browser\'s navbar'),
            'image_field'
        ),
    ),
])
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {'required': False}]
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
# CONSTANCE_DATABASE_CACHE_BACKEND = 'default'  // TODO: uncomment me when cache will be enabled
