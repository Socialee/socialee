from django import forms
from django.contrib import admin, auth
from django.utils.translation import ugettext_lazy as _

from .models import *



# admin.site.register(UserEntry)
# admin.site.register(Origin)
# admin.site.register(Profile)
# admin.site.register(Zettel)
# admin.site.register(InputOutput)
# admin.site.register(Input)
# admin.site.register(Output)
# admin.site.register(Project)






class InputZettelInline(admin.TabularInline):
    model = Input
    exclude = ('profile',)


class OutputZettelInline(admin.TabularInline):
    model = Output
    exclude = ('profile',)


class InputProfileInline(admin.TabularInline):
    model = Input
    exclude = ('zettel',)


class OutputProfileInline(admin.TabularInline):
    model = Output
    exclude = ('zettel',)


class ZettelInline(admin.TabularInline):
    model = Zettel
    exclude = ('inputs', 'outputs')
    extra = 1


class InputAdmin(admin.ModelAdmin):
    model = Input


class OutputAdmin(admin.ModelAdmin):
    model = Output


class ProjectAdmin(admin.ModelAdmin):
    model = Project


class ZettelAdmin(admin.ModelAdmin):
    model = Zettel
    search_fields = ['profile__user__username', 'profile__user__email',
                     'profile__user__last_name', 'profile__user__first_name',
                     'number', 'origin__location']
    list_filter = ['origin', 'origin__location']
    list_display = ['__str__', 'image', 'origin']
    inlines = [
        InputZettelInline, OutputZettelInline,
    ]


class OriginAdmin(admin.ModelAdmin):
    model = Origin


class ProfileAdmin(admin.ModelAdmin):
    pass


class UserEntryForm(forms.ModelForm):
    """Special form for UserEntryAdmin."""
    class Meta:
        model = UserEntry
        fields = '__all__'


class UserEntryAdmin(auth.admin.UserAdmin):
    """Special Admin: Use the "change" form also for adding new users."""
    add_form = UserEntryForm

    readonly_fields = ['last_login']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(auth.admin.UserAdmin, self).get_fieldsets(request, obj)

        # Remove specific fields.
        fieldsets = list(fieldsets)
        # Remove "password".
        assert fieldsets[0][0] is None
        fieldsets[0] = (None, {'fields': ('username',)})

        # All from Permissions, but keep "is_active".
        assert fieldsets[2][0] == _('Permissions')
        fieldsets[2] = (_('Permissions'), {'fields': ('is_active',)})
        return fieldsets


class ProfileEntryAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email', 'user__last_name',
                     'user__first_name']
    list_filter = ['plz', 'newsletter', 'zettel__origin__location']

    list_display = ['__str__', 'user_last_name', 'user_first_name',
                    'user_email']
    inlines = [
        InputProfileInline, OutputProfileInline
    ]

admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Origin, OriginAdmin)
admin.site.register(Profile, ProfileEntryAdmin)
admin.site.register(UserEntry, UserEntryAdmin)
admin.site.register(Zettel, ZettelAdmin)
