from django.conf import settings
from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns # not used right now
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

from socialee import views
from . import allauth_urls

urlpatterns = [
    
    url(r'^landingpage/', include('landingpage.urls')), # ID 000

    url(r'^accounts/', include('allauth.urls')), # IDs 081, 082, 083, etc
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)), # ID 900
    url(r'^blog/', include('zinnia.urls')), # IDs 050, 051, 052, etc
    url(r'^comments/', include('django_comments.urls')), # für Blog
    url(r'^feedback/', include("feedback.urls")), # Feedback-App
    url(r'^', include('ideas.urls')), # TODO IDs vergeben
    url(r'^impressum/$', views.Impressum.as_view(), name='impressum'), # ID 021
    url(r'^registrieren/', include('waitinglist.urls')), # ID 080
    url(r'^protect/', include('simple_auth.urls')), # password-protection for staging-server
    url(r'^question/', include('questions.urls')), # inaktiv, future feature
    url(r'^summernote/', include('django_summernote.urls')), # für Blog
    url(r'^zitat/', include('quotes.urls')), # ID 024

    # LOGIN REQUIRED
    url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # ID 100
    url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'), # ID 101
    url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectView.as_view()), name='project_view'), # ID 102
    url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(views.ProjectUpdateView.as_view()), name='project_updateview'), # ID 103
    
    url(r'^startprofile/$', login_required(views.StartProfile.as_view()), name='startprofile'),
    url(r'^profile/(?P<slug>[\w.@+-]+)/willkommen/$', login_required(views.WelcomePage.as_view()), name='welcome'), # ID 200
    url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'), # ID 203
    url(r'^profile/(?P<slug>[\w.@+-]+)/edit/$', login_required(views.ProfileUpdateView.as_view()), name='profile_updateview'), # ID 201

    #face view for user interagtion
    #url(r'^profile/(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),
    url(r'^comment/$', login_required(views.Comment.as_view()), name='comment'),
    url(r'^follow/$', login_required(views.Follow.as_view()), name='comment'),
]

if settings.DEBUG or not settings.PROD:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

