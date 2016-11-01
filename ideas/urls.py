from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.idea_list, name='idea_list'),
    url(r'^neu/$', views.CreateIdea.as_view(), name='create_idea'),
    url(r'^like/$', views.Like.as_view(), name='like'),
]