from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='question_home'),
    url(r'^(?P<id>\d+)/$', views.single, name='question_single'),
]