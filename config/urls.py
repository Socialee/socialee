from django.conf import settings
from django.conf.urls import include, url
# from django.conf.urls.i18n import i18n_patterns # not used right now
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

from socialee import views

if settings.DEBUG:
    urlpatterns = [
        
        url(r'^$', views.Home.as_view(), name='home'),
        url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        url(r'^accounts/', include('allauth.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^summernote/', include('django_summernote.urls')),
        url(r'^question/', include('questions.urls')),
        url(r'^quotes/', include('quotes.urls')),
        url(r'^blog/', include('zinnia.urls')),
        url(r'^comments/', include('django_comments.urls')),
        url(r'^invite_me/$', views.Invite_me, name='invite_me'),
        url(r'^impressum/$', views.Impressum.as_view(), name='impressum'),
        url(r'^welcome/(?P<slug>[\w.@+-]+)/$', login_required(views.WelcomePage.as_view()), name='welcome'), # login required!
        url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # login required!
        url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'),
        url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectDetailView.as_view()), name='project_detailview'),
        url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(views.ProjectUpdateView.as_view()), name='project_updateview'),
        url(r'^(?P<slug>[\w.@+-]+)/profile/update/$', login_required(views.ProfileUpdateView.as_view()), name='update_profile'),
        url(r'^(?P<slug>[\w.@+-]+)/profile/detail/$', login_required(views.ProfileDetailView.as_view()), name='profile_detail'),
        url(r'^(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'),
        url(r'^(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),

        # At the end, for django-cms.
        # Ref: https://django-cms.readthedocs.org/en/latest/how_to/install.html#url-configuration
        url(r'^', include('cms.urls')),
    ]

if not settings.DEBUG:
    urlpatterns = [
        
        url(r'^$', views.Home.as_view(), name='home'),
        url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        url(r'^accounts/', include('allauth.urls')),
        url(r'^admin/', include(admin.site.urls)),
        # url(r'^summernote/', include('django_summernote.urls')),
        # url(r'^question/', include('questions.urls')),
        # url(r'^quotes/', include('quotes.urls')),
        # url(r'^blog/', include('zinnia.urls')),
        # url(r'^comments/', include('django_comments.urls')),
        url(r'^invite_me/$', views.Invite_me, name='invite_me'),
        url(r'^impressum/$', views.Impressum.as_view(), name='impressum'),
        # url(r'^welcome/(?P<slug>[\w.@+-]+)/$', login_required(views.WelcomePage.as_view()), name='welcome'), # login required!
        # url(r'^startproject/$', login_required(views.StartProject.as_view()), name='startproject'), # login required!
        # url(r'^project_overview/$', views.ProjectOverview.as_view(), name='project_overview'),
        # url(r'^project/(?P<slug>[-\w]+)/$', login_required(views.ProjectDetailView.as_view()), name='project_detailview'),
        # url(r'^project/(?P<slug>[-\w]+)/edit/$', login_required(views.ProjectUpdateView.as_view()), name='project_updateview'),
        # url(r'^(?P<slug>[\w.@+-]+)/profile/update/$', login_required(views.ProfileUpdateView.as_view()), name='update_profile'),
        # url(r'^(?P<slug>[\w.@+-]+)/profile/detail/$', login_required(views.ProfileDetailView.as_view()), name='profile_detail'),
        # url(r'^(?P<slug>[\w.@+-]+)/$', login_required(views.ProfileView.as_view()), name='profile_view'),
        # url(r'^(?P<slug>[\w.@+-]+)/socialeebhaber/$', login_required(views.Socialeebhaber.as_view()), name='socialeebhaber'),

        # At the end, for django-cms.
        # Ref: https://django-cms.readthedocs.org/en/latest/how_to/install.html#url-configuration
        url(r'^', include('cms.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)