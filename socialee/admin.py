import datetime
from django import forms
from django.contrib import admin, auth
from django.forms import TextInput, Textarea
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import *

from embed_video.admin import AdminVideoMixin


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


class ProjectAdmin(AdminVideoMixin, admin.ModelAdmin):
    model = Project
    list_display = ['title', 'created_by']
    fields = (('created_by', 'slug'), 'picture', ('title', 'tagline'), 'description', 'location', 'tags', 'video', 'longdescription', 'history', 'managers')
    readonly_fields = ('created_by', 'slug')
    inlines = [
        OutputInline,
        InputInline,
        ]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['created_by', 'user_email', 'user_full_name']
    fields = (('created_by', 'picture'), 'tags', 'tagline', 'description', ('phone', 'plz', 'newsletter'))
    inlines = [
        OutputInline,
        InputInline,
        ]


class UserDataAdmin( admin.ModelAdmin):
    model = UserData
    list_display = ['user', 'thumb', 'dateJoined']

#admin.site.register(CommonGround, CommonGroundAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserData, UserDataAdmin)

## unregister Apps that are not used in Admin
# from django.contrib.sites.models import Site
# admin.site.unregister(Site)

# from django_comments.models import Comment
# admin.site.unregister(Comment)

# from allauth.socialaccount.models import *
# admin.site.unregister(SocialAccount)
# admin.site.unregister(SocialToken)
# admin.site.unregister(SocialApp)

# from tagging.models import *
# admin.site.unregister(Tag)
# admin.site.unregister(TaggedItem)

# from taggit.models import *
# admin.site.unregister(Tag)