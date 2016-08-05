# encoding: utf-8

import re
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.http import urlencode


class SimpleAuthMiddleware(object):
    """
    Middleware class checks provided URL patterns to protect URLs and allows
    both authenticated users to access protected URLs and anonymous users who
    have entered a valid password.
    """

    def allow_user(self, request):
        if request.user.is_authenticated():
            return True
        if request.session.get('simple_auth'):
            return True
        return False

    def process_request(self, request):
        if self.allow_user(request):
            return None

        IGNORE = getattr(settings, 'SIMPLE_AUTH_IGNORE', [r'^admin/'])
        PROTECT = getattr(settings, 'SIMPLE_AUTH_PROTECT', [])

        if reverse('simple_auth_password') in request.path:
            return None

        # Strip leading slash
        search_path = request.path[1:]

        for ignored_pattern in IGNORE:
            if re.match(ignored_pattern, search_path):
                return None

        if PROTECT:
            for protected_pattern in PROTECT:
                print(protected_pattern, search_path)
                if re.match(protected_pattern, search_path):
                    return redirect("{0}?{1}".format(
                        reverse('simple_auth_password'),
                        urlencode({'url': request.path}),
                    ))
            return None

        return redirect("{0}?{1}".format(
            reverse('simple_auth_password'),
            urlencode({'url': request.path}),
        ))
