import datetime
from django import forms
from django.contrib import admin, auth
from django.forms import TextInput, Textarea
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import *




class InputInline(admin.TabularInline):
    model = Input
    extra = 3
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':50})},
    }


class OutputInline(admin.TabularInline):
    model = Output
    extra = 3
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':50})},
    }


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['title', 'created_by']
    fields = ('created_by', 'title', 'tagline', 'description', 'header_img', 'tags', 'managers')


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'user_email', 'user_full_name']
    fields = (('user', 'picture'), 'tags', 'tagline', 'description', ('phone', 'plz', 'newsletter'), 'inputs', 'outputs')
    inlines = [
        OutputInline,
        InputInline,
        ]




admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Input, InputAdmin)
# admin.site.register(Invite, InviteAdmin)



### Not in use right now but still here for as an example

# class CommonGroundAdmin(admin.ModelAdmin):
#     model = CommonGround
#     fields = ('slug', 'tagline', 'tags', 'inputs', 'outputs')

# def mark_as_done(modeladmin, request, queryset):
#     queryset.update(done=True)
# mark_as_done.short_description = "Alle markierten als erledigt markieren"

# class InviteAdmin(admin.ModelAdmin):
#     list_display = ('was_submitted_recently','done','full_name', 'email', 'message')
#     list_display_links = ['email']
#     # list_editable = ['done']
#     actions = [mark_as_done]