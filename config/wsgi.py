"""
WSGI config for socialee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


# For Heroku. (old settings with dj-static, also see: Procfile in root-folder!)
# try:
#     from dj_static import Cling, MediaCling
#     application_with_static = Cling(MediaCling(application))
# except ImportError:
#     pass
