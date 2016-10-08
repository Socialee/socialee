from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NewsletterSignup.as_view(), name='waitinglist'), # ID 080
]