"""
Django settings for socialee project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

TODO: use django-configurations, for class based approach?!
"""
# -*- coding: utf-8 -*-
import os
import environ

gettext = lambda s: s

# Build paths inside the project like this: os.path.join(ROOT_DIR, ...)
ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('socialee')

assert os.path.exists(str(ROOT_DIR.path("Makefile"))), "ROOT_DIR is (not?) set properly."

CMS_TEMPLATES = (
    ('home.html', 'Home / Landingpage'),
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
SIMPLE_AUTH = env.bool('SIMPLE_AUTH', False)
INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = (
    # DJANGO APPS
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
    'treebeard',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for JavaScript and CSS management

    # Zinnia requirements.
    'mptt',  # utilities for implementing a tree
    'tagging',
    'django_comments',
    'ckeditor',

    # 'reversion', # version-conflicts with cms (http://docs.django-cms.org/en/latest/how_to/install.html)
    'djangocms_file',
    'djangocms_flash',
    #'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'djangocms_link',
    'djangocms_text_ckeditor',
    'djangocms_snippet',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',

    # THIRD PARTY APPS
    'betterforms', # works only in Version 1.1.2
    'crispy_forms',
    'crispy_forms_foundation',
    'django_summernote',
    'simple_auth',
    'taggit',
    'zinnia',
    'zinnia_ckeditor',

    # SOCIALEE CUSTOM APPS
    'questions.apps.QuestionsConfig',
    'quotes.apps.QuotesConfig',
    'socialee.apps.SocialeeConfig',
)

if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',  # use always included jQuery.
}

MIDDLEWARE_CLASSES = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'cms.middleware.utils.ApphookReloadMiddleware',
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
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Password Protection for Staging Server
# SIMPLE_AUTH = False
if SIMPLE_AUTH==True: # set in socialee-stage.herokuapp.com
    MIDDLEWARE_CLASSES += [
    'simple_auth.middleware.SimpleAuthMiddleware',
    ]

    SIMPLE_AUTH_IGNORE = [
        r'^admin/',
    ]

    SIMPLE_AUTH_PROTECT = [
        r'^$',
    ]

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
                'django.template.context_processors.i18n',
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
            'debug': env.bool('DJANGO_TEMPLATE_DEBUG', DEBUG),
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# for local. defined in environment
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env.str('DJANGO_EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = env.str('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_HOST_USER', '')
EMAIL_PORT = env.str('DJANGO_EMAIL_PORT', '')
DEFAULT_FROM_EMAIL = env.str('DJANGO_FROM_EMAIL', 'webmaster@localhost')
SERVER_EMAIL = env.str('DJANGO_FROM_EMAIL', 'root@localhost')
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
    'login': 'socialee.forms.SocialeeLoginForm'
}

SOCIALACCOUNT_ENABLED = False

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = str(ROOT_DIR('media'))
STATIC_ROOT = str(ROOT_DIR('build', 'static'))
STATICFILES_DIRS = (str(APPS_DIR('static')), )

# Configure SSL for Heroku and force redirect to https.
# > heroku config:set --app socialee-staging DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
# > heroku config:set --app socialee-staging DJANGO_SECURE_SSL_REDIRECT=1
SECURE_PROXY_SSL_HEADER = tuple(env.list('DJANGO_SECURE_PROXY_SSL_HEADER', default=[]))
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', False)

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

# Add 'foundation-5' layout pack
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'foundation-5') # F5 works for F6 as well
# Default layout to use with "crispy_forms"
CRISPY_TEMPLATE_PACK = 'foundation-5'

# Zinnia Blog Settings
ZINNIA_ENTRY_CONTENT_TEMPLATES = [
            ('zinnia/_entry_detail_alternate.html', gettext('Alternative template')),
            ]
ZINNIA_ENTRY_DETAIL_TEMPLATES = [
            ('entry_detail_alternate.html', gettext('Alternative template')),
            ]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
    },
    'zinnia-content': {
        'toolbar_Zinnia': [
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
            ['Undo', 'Redo'],
            ['Scayt'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Source'],
            ['Maximize'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike',
             'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-',
             'Outdent', 'Indent', '-', 'Blockquote'],
            ['Styles', 'Format'],
        ],
        'toolbar': 'Zinnia',
    },
}