from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from socialee import views

urlpatterns = i18n_patterns('',
    url(r'^', include('cms.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


# und so steht's in den cms-docs:

# urlpatterns = i18n_patterns('',
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^', include('cms.urls')),
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)