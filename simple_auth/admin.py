from django.contrib import admin
from .models import Password
from config import settings

if settings.STAGE:
	admin.site.register(Password)
