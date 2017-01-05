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

class FollowsInline(admin.TabularInline):
    model = CommonGround.inst_follower.through
    fk_name = "to_commonground"
    extra = 1


class ProjectAdmin(AdminVideoMixin, admin.ModelAdmin):
    model = Project
    list_display = ['title', 'created_by']
    fields = ('picture', ('title', 'tagline'), 'description', 'location', 'tags', 'video', 'longdescription', 'history', 'managers')
    inlines = [
        FollowsInline,
        OutputInline,
        InputInline,
        ]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['created_by', 'user_email', 'user_full_name']
    fields = (('created_by', 'picture'), 'tags', 'tagline', 'description', ('phone', 'plz', 'newsletter'))
    inlines = [
        FollowsInline,
        OutputInline,
        InputInline,
        ]

class CommonGroundAdmin(admin.ModelAdmin):
    model = CommonGround
    list_display = ['slug']
    fields = (('created_by', 'picture'), 'tags', 'tagline', 'description')
    inlines = [
        FollowsInline,
        ]


#admin.site.register(CommonGround, CommonGroundAdmin)
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