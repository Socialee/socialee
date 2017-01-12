from django.conf.urls import url

from .views import simple_password


urlpatterns = [
	url(r'^$', view=simple_password, name="simple_auth_password"),
	]
	
