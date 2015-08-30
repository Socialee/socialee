"""
Django settings for socialee project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

TODO: use django-configurations, for class based approach?!
"""

import os

import environ

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('socialee')
# APPEND_SLASH = False # TODO: get rid of trailing slash

assert os.path.exists(str(ROOT_DIR.path("Makefile"))), "ROOT_DIR is set properly."

CMS_TEMPLATES = (
    ('empty_template.html', 'Empty Template'),
    ('project_template.html', 'Project Template'),
)

env = environ.Env()

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY',
                     'gx)-+#9(hotw=qt@swr170k3!l*!=a%6&+)siw4$0q35egtj(1')

DEBUG = env.bool('DJANGO_DEBUG', False)
INTERNAL_IPS = ('127.0.0.1',)
TEMPLATE_DEBUG = env.bool('DJANGO_TEMPLATE_DEBUG', DEBUG)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',  # for the admin skin. Before 'django.contrib.admin'.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    # Base django-cms requirements.
    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    'treebeard',

    'reversion',
    'djangocms_file',
    'djangocms_flash',
    # 'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'djangocms_link',
    'djangocms_snippet',
    'djangocms_text_ckeditor',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'django_comments',
    'tagging',
    'zinnia',
    # 'cmsplugin_zinnia', not yet compatible with  v1.8

    # Main app.
    'socialee',
)

if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
        'debug_toolbar',
    )

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',  # use always included jQuery.
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR('templates'))],
        'OPTIONS': {
            # NOTE: app_namespace.Loader can not work properly if you use it in conjunction with django.template.loaders.cached.Loader and inheritance based on empty namespaces.
            #       (README at https://github.com/Fantomas42/django-app-namespace-template-loader)
            'loaders': ['app_namespace.Loader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                       ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'zinnia.context_processors.version',  # Optional
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# for local. defined in envronment
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env.str('DJANGO_EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = env.str('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_HOST_USER', '')
EMAIL_PORT = env.str('DJANGO_EMAIL_PORT', '')
DEFAULT_FROM_EMAIL = env.str('DJANGO_FROM_EMAIL')
SERVER_EMAIL = env.str('DJANGO_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = 'Socialee meldet: '
if EMAIL_PORT == '465':
    EMAIL_USE_SSL = True

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db("DATABASE_URL", default="sqlite:///db.sqlite3"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

MIGRATION_MODULES = {
    # For non-ported Django-CMS plugins.
    # Ref: https://django-cms.readthedocs.org/en/latest/how_to/install.html
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_video': 'djangocms_video.migrations_django',
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('de', 'German'),
]

# auth and allauth settings
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'SCOPE': ['email', 'public_profile', 'user_friends'],
        'METHOD': 'js_sdk',
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        # 'LOCALE_FUNC': 'path.to.callable',
        # 'VERIFIED_EMAIL': False,
        # 'VERSION': 'v2.3'
        }
    }
ACCOUNT_FORMS = {
    'signup': 'socialee.forms.MySignupForm',
}
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = str(ROOT_DIR('media'))
STATIC_ROOT = str(ROOT_DIR('build', 'static'))
STATICFILES_DIRS = (str(APPS_DIR('static')), )

# Add django-sslify on Heroku, based on env setting.
# > heroku config:set --app socialee-staging DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_PROXY_SSL_HEADER = tuple(env.list('DJANGO_SECURE_PROXY_SSL_HEADER', []))
if SECURE_PROXY_SSL_HEADER:
    MIDDLEWARE_CLASSES = ['sslify.middleware.SSLifyMiddleware'] + \
        MIDDLEWARE_CLASSES

# Configure logging, especially for Heroku.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}
