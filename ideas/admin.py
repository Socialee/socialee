import datetime

from django.contrib import admin
from django.utils import timezone
from .models import Idea, Comment

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(active=True)
    make_published.short_description = "Alle markierten Ideen veröffentlichen"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(active=False)
    make_unpublished.short_description = "Veröffentlichung zurücknehmen"

class CommentInline(admin.TabularInline):
    model = Comment

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('was_submitted_recently', 'private', 'active', 'featured', 'title',  'author', 'thumb')
    list_display_links = ['title']
    list_editable = ['featured']
    fields = [('private', 'active', 'featured', 'thumb', 'picture'), ('title', 'author'), 'description', 'likes']
    list_filter = ['subm_date', 'author']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ('likes', 'thumb', 'private')
    inlines = [
        CommentInline,
    ]

    actions = [make_published, make_unpublished]

admin.site.register(Idea, IdeaAdmin)