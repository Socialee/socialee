from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IdeaListView.as_view(), name='idea_list'),
    url(r'^neu/$', views.CreateIdea.as_view(), name='create_idea'),
    url(r'^idea_like/$', views.Like.as_view(), name='idea_like'),
    url(r'^idea_comment/$', views.Commentate.as_view(), name='idea_comment'),
    url(r'^(?P<pk>\d+)$', views.IdeaDetailView.as_view(), name='idea_detail'),
    url(r'^edit/(?P<pk>\d+)$', views.IdeaEditView.as_view(), name='idea_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.IdeaDeleteView.as_view(), name='delete_idea'),
]