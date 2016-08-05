from django.conf.urls import patterns, url

from .views import simple_password


urlpatterns = patterns('',
    url(r'^$', view=simple_password, name="simple_auth_password"),
)
