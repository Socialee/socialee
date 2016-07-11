import datetime
from django import forms
from django.contrib import admin, auth
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import *


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['title', 'created_by']
    fields = ('created_by', 'title', 'tagline', 'description', 'header_img', 'managers')


def mark_as_done(modeladmin, request, queryset):
    queryset.update(done=True)
mark_as_done.short_description = "Alle markierten als erledigt markieren"

class InviteAdmin(admin.ModelAdmin):
    list_display = ('was_submitted_recently','done','full_name', 'email', 'message')
    list_display_links = ['email']
    # list_editable = ['done']
    actions = [mark_as_done]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Invite, InviteAdmin)
