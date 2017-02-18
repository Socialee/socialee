from django.contrib.auth.models import User
from .models import Project
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy

def user_is_project_manager(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Project.objects.get(slug=kwargs['slug'])
            if request.user in obj.managers.all():
                return function(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator(function)


def user_is_profile_owner(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Profile.objects.get(slug=kwargs['slug'])
            if request.user == obj.created_by:
                return function(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator(function)

def user_is_request_user(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.username == kwargs['slug']:
                return function(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator(function)