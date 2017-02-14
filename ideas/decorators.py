from django.contrib.auth.models import User
from ideas.models import Idea
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy

def is_idea_not_private(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Idea.objects.get(id=kwargs['pk'])
            if obj.private:
                if not hasattr(request.user, 'email'):
                    return HttpResponseForbidden()
                if obj.author != request.user.email:
                    return HttpResponseForbidden()
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)

def user_is_idea_author(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Idea.objects.get(id=kwargs['pk'])
            if not hasattr(request.user, 'email'):
                return HttpResponseForbidden()
            if obj.author != request.user.email:
                return HttpResponseForbidden()
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)