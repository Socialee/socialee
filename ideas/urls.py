from django.conf.urls import url
from .decorators import is_idea_not_private, user_is_idea_author

from . import views

urlpatterns = [
    url(r'^$', views.IdeaListView.as_view(), name='idea_list'),
    url(r'^neu/$', views.CreateIdea.as_view(), name='create_idea'),
    url(r'^idea_like/$', views.Like.as_view(), name='idea_like'),
    url(r'^idea_comment/$', views.Commentate.as_view(), name='idea_comment'),
    url(r'^(?P<pk>\d+)$', is_idea_not_private(views.IdeaDetailView.as_view()), name='idea_detail'),
    url(r'^edit/(?P<pk>\d+)$', user_is_idea_author(views.IdeaEditView.as_view()), name='idea_edit'),
    url(r'^delete/(?P<pk>\d+)$', user_is_idea_author(views.IdeaDeleteView.as_view()), name='delete_idea'),
]