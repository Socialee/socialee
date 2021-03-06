from django.conf import settings
from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns # not used right now
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

from register.views import password_change
from socialee import views
from . import allauth_urls

from socialee.decorators import user_is_project_manager, user_is_profile_owner, user_is_request_user

urlpatterns = [
    
    url(r'^', include('landingpage.urls')), # ID 000

    url(r'^accounts/password/change/$', login_required(password_change), name='password_change'),
    url(r'^accounts/', include('allauth.urls')), # IDs 081, 082, 083, etc
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)), # ID 900
    url(r'^blog/', include('zinnia.urls')), # IDs 050, 051, 052, etc
    url(r'^comments/', include('django_comments.urls')), # für Blog
    url(r'^feedback/', include("feedback.urls")), # Feedback-App
    url(r'^ideen/', include('ideas.urls')), # TODO IDs vergeben
    url(r'^impressum/$', views.Impressum.as_view(), name='impressum'), # ID 021
    url(r'^registrieren/', include('register.urls'), name='register'), # ID 080
    url(r'^protect/', include('simple_auth.urls')), # password-protection for staging-server
    url(r'^question/', include('questions.urls')), # inaktiv, future feature
    url(r'^summernote/', include('django_summernote.urls')), # für Blog
    url(r'^styleguide/$', views.Styleguide.as_view(), name='styleguide'),
    url(r'^zitat/', include('quotes.urls')), # ID 024

    # LOGIN REQUIRED
    url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # ID 100
    url(r'^startproject/(?P<idea>\w+)$', login_required(views.StartProject.as_view()), name='startprojectWithIdea'), 
    url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'), # ID 101
    url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectView.as_view()), name='project_view'), # ID 102
    url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(user_is_project_manager(views.ProjectUpdateView.as_view())), name='project_updateview'), # ID 103
    
    url(r'^startprofile/$', login_required(views.StartProfile.as_view()), name='startprofile'),
    url(r'^profile/(?P<slug>[\w.@+-]+)/willkommen/$', login_required(user_is_request_user(views.WelcomePage.as_view())), name='welcome'), # ID 200
    url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'), # ID 203
    url(r'^profile/(?P<slug>[\w.@+-]+)/edit/$', login_required(user_is_profile_owner(views.ProfileUpdateView.as_view())), name='profile_updateview'), # ID 201

    url(r'^user/(?P<slug>[\w.@+-]+)/edit/$', login_required(user_is_request_user(views.UserUpdateView.as_view())), name='user_updateview'), # ID 201

    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^activity/', include('actstream.urls')),

    #face view for user interagtion
    #url(r'^profile/(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),
    url(r'^comment/$', login_required(views.Comment.as_view()), name='comment'),
    url(r'^follow/$', login_required(views.Follow.as_view()), name='comment'),
    url(r'^actAs/$', login_required(views.ActAs.as_view()), name='actAs'),
    url(r'^like/$', login_required(views.Like.as_view()), name='like_message'),
]

if not settings.PROD:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)