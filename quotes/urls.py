from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.create_quote, name='make_quote'),
    url(r'^show-all-quotes/$', views.show_all_quotes, name='show_quote'),
]