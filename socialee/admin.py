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
    fields = ('created_by', 'title', 'tagline', 'description', 'picture', 'tags', 'managers')
    inlines = [
        OutputInline,
        InputInline,
        ]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['created_by', 'user_email', 'user_full_name']
    fields = (('created_by', 'picture'), 'tags', 'tagline', 'description', 'follows', ('phone', 'plz', 'newsletter'))
    inlines = [
        OutputInline,
        InputInline,
        ]




admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)

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