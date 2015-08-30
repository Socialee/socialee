from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from socialee import views

urlpatterns = i18n_patterns(
    '',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^impressum/$', views.Impressum.as_view(), name='impressum'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^projekte/antonsreise/$', views.Jumpage.as_view(), name='jumpage'),

    # At the end, for django-cms.
    # Ref: https://django-cms.readthedocs.org/en/latest/how_to/install.html#url-configuration
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
