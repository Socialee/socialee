from django.contrib import admin
from .models import Landingpage


class LandingpageAdmin(admin.ModelAdmin):
    list_display = ('claim', 'active')

admin.site.register(Landingpage, LandingpageAdmin)