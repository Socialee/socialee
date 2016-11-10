from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.idea_list, name='idea_list'),
    url(r'^neu/$', views.CreateIdea.as_view(), name='create_idea'),
    url(r'^idea_like/$', views.Like.as_view(), name='idea_like'),
    url(r'^idea_comment/$', views.Commentate.as_view(), name='idea_comment'),
]