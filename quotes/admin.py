import datetime

from django.contrib import admin
from django.utils import timezone
from .models import Quote

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(active=True)
make_published.short_description = "Alle markierten Zitate veröffentlichen"


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('was_submitted_recently', 'active', 'author', 'title')
    list_display_links = ['title']
    list_editable = ['active']
    list_filter = ['subm_date', 'author']
    search_fields = ['author', 'title']
    actions = [make_published]

admin.site.register(Quote, QuoteAdmin)