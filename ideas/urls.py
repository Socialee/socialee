from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.create_idea, name='create_idea'),
    url(r'^(?P<id>\d+)/details/$', views.idea_details, name='idea_details'),
    url(r'^(?P<id>\d+)/autor/$', views.idea_author, name='idea_author'),
    url(r'^galerie/$', views.idea_list, name='idea_list'),
]