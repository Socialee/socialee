from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin


from socialee import views

import allauth

admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}),
	url(r'^accounts/', include('allauth.urls')),
    url(r'^projects/', include('cms.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)