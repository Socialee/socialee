import datetime

from django.contrib import admin
from django.utils import timezone
from .models import Idea, Comment

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(enabled=True)
make_published.short_description = "Idee veröffentlichen"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(enabled=False)
make_unpublished.short_description = "Veröffentlichung zurücknehmen"

def feature(modeladmin, request, queryset):
    queryset.update(featured=True)
    queryset.update(enabled=True)
feature.short_description = "Idee featuren"

def unfeature(modeladmin, request, queryset):
    queryset.update(featured=False)
unfeature.short_description = "Idee unfeaturen"

class CommentInline(admin.TabularInline):
    model = Comment

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('was_submitted_recently', 'enabled', 'featured', 'title', 'private', 'author', 'thumb', 'active')
    list_display_links = ['title', 'was_submitted_recently', 'thumb']
    fields = [('private', 'enabled', 'featured', 'thumb', 'picture'), ('title', 'author'), 'description', 'likes']
    list_filter = ['subm_date', 'author']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ('likes', 'thumb', 'private', 'active')
    inlines = [
        CommentInline,
    ]

    actions = [make_published, feature, unfeature, make_unpublished]

admin.site.register(Idea, IdeaAdmin)