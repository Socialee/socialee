from django.conf import settings
from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns # not used right now
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

from socialee import views
from . import allauth_urls

if settings.DEBUG or settings.SIMPLE_AUTH:
    urlpatterns = [
        
        url(r'^', include('landingpage.urls')), # ID 000

        url(r'^accounts/', include('allauth.urls')), # IDs 081, 082, 083, etc
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)), # ID 900
        url(r'^blog/', include('zinnia.urls')), # IDs 050, 051, 052, etc
        url(r'^comments/', include('django_comments.urls')), # für Blog
        url(r'^ideen/', include('ideas.urls')), # TODO IDs vergeben
        url(r'^impressum/$', views.Impressum.as_view(), name='impressum'), # ID 021
        url(r'^warteliste/$', views.NewsletterSignup.as_view(), name='invite_me'), # ID 080
        url(r'^protect/', include('simple_auth.urls')), # password-protection for staging-server
        url(r'^question/', include('questions.urls')), # inaktiv, future feature
        url(r'^summernote/', include('django_summernote.urls')), # für Blog
        url(r'^zitat/', include('quotes.urls')), # ID 024

        url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # ID 100
        url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'), # ID 101
        url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectView.as_view()), name='project_view'), # ID 102
        url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(views.ProjectUpdateView.as_view()), name='project_updateview'), # ID 103
        
        url(r'^profile/(?P<slug>[\w.@+-]+)/willkommen/$', login_required(views.WelcomePage.as_view()), name='welcome'), # ID 200
        url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'), # ID 203
        url(r'^profile/(?P<slug>[\w.@+-]+)/edit/$', login_required(views.ProfileUpdateView.as_view()), name='profile_updateview'), # ID 201

        #face view for user interagtion
        url(r'^profile/(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),
        url(r'^comment/$', login_required(views.Comment.as_view()), name='comment'),

        # DjangoCMS, keep this always at the end
        url(r'^', include('cms.urls')), 
    ]

if not settings.DEBUG and not settings.SIMPLE_AUTH:
    urlpatterns = [

        url(r'^$', views.Home.as_view(), name='home'), # ID 000

        url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        url(r'^accounts/', include(allauth_urls.allauth_patterns)),

        # url(r'^accounts/', include('allauth.urls')), # IDs 081, 082, 083, etc
        url(r'^admin/', include(admin.site.urls)), # ID 900
        url(r'^blog/', include('zinnia.urls')), # IDs 050, 051, 052, etc
        url(r'^comments/', include('django_comments.urls')), # für Blog
        url(r'^impressum/$', views.Impressum.as_view(), name='impressum'), # ID 021
        url(r'^warteliste/$', views.NewsletterSignup.as_view(), name='invite_me'), # ID 080
        # url(r'^question/', include('questions.urls')), # inaktiv, future feature
        url(r'^summernote/', include('django_summernote.urls')), # für Blog
        url(r'^zitat/', include('quotes.urls')), # ID 024

        # url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # ID 100
        # url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'), # ID 101
        # url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectDetailView.as_view()), name='project_detailview'), # ID 102
        # url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(views.ProjectUpdateView.as_view()), name='project_updateview'), # ID 103
        
        # url(r'^profile/(?P<slug>[\w.@+-]+)/willkommen/$', login_required(views.WelcomePage.as_view()), name='welcome'), # ID 200
        # url(r'^profile/(?P<slug>[\w.@+-]+)/edit/$', login_required(views.ProfileUpdateView.as_view()), name='update_profile'), # ID 201
        # url(r'^profile/(?P<slug>[\w.@+-]+)/detail/$', login_required(views.ProfileDetailView.as_view()), name='profile_detail'), # ID 202
        # url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'), # ID 203
        # url(r'^profile/(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),

        # DjangoCMS, keep this always at the end
        url(r'^', include('cms.urls')),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)