import datetime

from django.contrib import admin
from django.utils import timezone
from .models import Idea

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(active=True)
    make_published.short_description = "Alle markierten Ideen veröffentlichen"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(active=False)
    make_unpublished.short_description = "Veröffentlichung zurücknehmen"


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('was_submitted_recently', 'active', 'author', 'title')
    list_display_links = ['title']
    # list_editable = ['active']
    list_filter = ['subm_date', 'author']
    search_fields = ['author', 'title']
    actions = [make_published, make_unpublished]

admin.site.register(Idea, IdeaAdmin)