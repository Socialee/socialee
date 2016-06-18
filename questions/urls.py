from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', login_required(views.home), name='question_home'),
    url(r'^(?P<id>\d+)/$', login_required(views.single), name='question_single'),
]