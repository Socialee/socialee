from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.create_idea, name='create_idea'),
    url(r'^galerie/$', views.idea_list, name='idea_list'),
]