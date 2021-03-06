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

env = environ.Env()

SITE_ID = 1

# Error reporting messages are being sent to: (https://docs.djangoproject.com/en/1.9/howto/error-reporting/)
ADMINS = [('Sehera', 'sehera.nawaz@gmail.com'), ('Moritz', 'mail@moritzjuedes.de')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY',
                     'gx)-+#9(hotw=qt@swr170k3!l*!=a%6&+)siw4$0q35egtj(1')

DEBUG = env.bool('DJANGO_DEBUG', False)
STAGE = env.bool('STAGE', False)
PROD = env.bool('PROD', False)
LIVE = env.bool('LIVE', False)

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS = (
    'collectfast',
    # DJANGO APPS
    'djangocms_admin_style',  # for the admin skin. Before 'django.contrib.admin'.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Zinnia requirements.
    'mptt',  # utilities for implementing a tree
    'tagging',
    'django_comments',
    'ckeditor',

    # THIRD PARTY APPS
    'admin_reorder',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'debug_toolbar',
    'embed_video', # http://django-embed-video.readthedocs.io/en/v1.1.0/installation.html
    # 'django_summernote',
    'simple_auth',
    'sekizai',  # for JavaScript and CSS management
    'taggit',
    'zinnia',
    'zinnia_ckeditor',
    'storages',
    'invitations', # has to be after allauth

    # SOCIALEE CUSTOM APPS
    'feedback.apps.FeedbackConfig',
    'ideas.apps.IdeasConfig',
    'landingpage.apps.LandingpageConfig',
    'questions.apps.QuestionsConfig',
    'quotes.apps.QuotesConfig',
    'socialee.apps.SocialeeConfig',
    'register.apps.RegisterConfig',

    'actstream.apps.ActstreamConfig', #this has to be last
)

if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
        'django.contrib.admindocs',
    )

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

# AWS S3 Settings
if LIVE and not DEBUG:

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_STATIC_BUCKET_NAME = os.environ['AWS_STATIC_BUCKET_NAME']
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
      'Cache-Control': 'max-age=86400',
    }
    AWS_S3_HOST = "s3-eu-central-1.amazonaws.com"
    AWS_PRELOAD_METADATA = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'config.storage.S3StaticStorage'
    # these next two aren't used, but staticfiles will complain without them
    STATIC_URL = "https://%s.s3.amazonaws.com/" % AWS_STATIC_BUCKET_NAME
    MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
    STATIC_ROOT = ''

else:
    COLLECTFAST_ENABLED = False
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Password Protection for Staging Server
if STAGE==True: # set in socialee-stage.herokuapp.com
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
        'DIRS': [
                str(APPS_DIR('templates/')),
                str(APPS_DIR('templates/socialee/')),
                str(APPS_DIR('templates/socialee/cards/')),
                str(APPS_DIR('templates/socialee/project/')),
                str(APPS_DIR('templates/socialee/profile/')),
                str(APPS_DIR('templates/socialee/shared/')),
                str(APPS_DIR('templates/socialee/snippets/')),
                ],
        'OPTIONS': {
            # NOTE: app_namespace.Loader can not work properly if you use it in conjunction with django.template.loaders.cached.Loader and inheritance based on empty namespaces.
            #       (README at https://github.com/Fantomas42/django-app-namespace-template-loader)
            'loaders': ['app_namespace.Loader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                       ],
            'context_processors': [
                'socialee.context_processors.prod',
                'socialee.context_processors.live',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'sekizai.context_processors.sekizai',
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
EMAIL_SUBJECT_PREFIX = ''
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
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/accounts/password/set'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/password/set'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_LOGOUT_ON_GET = True # SECURITY RISK??? See: http://django-allauth.readthedocs.io/en/latest/views.html#logout

ACCOUNT_ADAPTER = "register.adapter.AdvancedMailAccountAdapter"

INVITATIONS_ALLOW_JSON_INVITES = True
INVITATIONS_SIGNUP_REDIRECT = 'register'

ACTSTREAM_SETTINGS = {
    'USE_JSONFIELD': True,
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

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
            'level': env.str('DJANGO_LOG_LEVEL', 'INFO'),
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

# # Add 'foundation-5' layout pack
# CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'foundation-5') # F5 works for F6 as well
# # Default layout to use with "crispy_forms"
# CRISPY_TEMPLATE_PACK = 'foundation-5'

# Zinnia Blog Settings
ZINNIA_PREVIEW_MAX_WORDS = 22
# ZINNIA_ENTRY_CONTENT_TEMPLATES = [
#             ('zinnia/_video_entry.html', gettext('Artikel mit Video')),
#             ]
# ZINNIA_ENTRY_DETAIL_TEMPLATES = [
#             ('entry_detail_alternate.html', gettext('Artikel mit Video')),
#             ]

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
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar', 'Smiley', 'Iframe'],
            ['Source'],
            ['Maximize'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike',
             'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['CreateDiv','NumberedList', 'BulletedList', '-',
             'Outdent', 'Indent', '-', 'Blockquote'],
            ['Styles', 'Format'],
        ],
        'toolbar': 'Zinnia',
    },
}

TELLME_FEEDBACK_EMAIL = 'feedback@socialee.de'
NEW_IDEA_EMAIL = 'hello@socialee.de'

# Debug Toolbar settings / http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html
from debug_toolbar import settings as dt_settings
CONFIG_DEFAULTS = {
    # Toolbar options
    'DISABLE_PANELS': set(['debug_toolbar.panels.redirects.RedirectsPanel']),
    'JQUERY_URL': '',
    'SHOW_COLLAPSED': True,
}

# Reorder Socialee Admin via: https://github.com/mishbahr/django-modeladmin-reorder
ADMIN_REORDER = (

    # Authentifcation
    {
    'app': 'auth',
    'label': 'Socialee-Nutzer',
    'models': (
        {
        'model': 'account.EmailAddress',
        'label': 'E-Mail-Adressen',
        },
        {
        'model': 'auth.User',
        'label': 'User',
        },
        {
        'model': 'socialee.UserData',
        'label': 'User Details',
        },
        {
        'model': 'auth.Group',
        'label': 'User-Gruppe',
        },
        {
        'model': 'invitations.Invitation',
        'label': 'Einladungen',
        }
        )},

    # Ideen
    {
    'app': 'ideas',
    'label': 'Ideen',
    'models': ({
        'model': 'ideas.Idea',
        'label': 'Ideen auf Socialee'
        },
        )},

    # Socialee Projekte & Profile
    {
    'app': 'socialee',
    'label': 'Profile & Projekte',
    'models': (
        {
        'model': 'socialee.Profile',
        'label': 'Profile',
        },
        {
        'model': 'socialee.Project',
        'label': 'Projekte',
        },
        # {
        # 'model': 'socialee.CommonGround',
        # 'label': 'CommonGround',
        # },
        )},

    # Blog
    'zinnia',

    # Sonstige
    {
    'app': 'quotes',
    'label': 'Sonstige',
    'models': (
        {
        'model': 'quotes.Quote',
        'label': 'Zitate',
        },
        {
        'model': 'feedback.Feedback',
        'label': 'Feedback',
        },
        {
        'model': 'actstream.Follow',
        'label': 'Follow',
        },
        )},

    # Put all other Apps here
    'simple_auth',
)