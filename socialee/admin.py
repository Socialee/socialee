from django.contrib import admin

from .models import Input, Output, Origin, Profile, Zettel
from .models import ProfileErfassung


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


class ProfileInline(admin.TabularInline):
    model = Profile


class ZettelInline(admin.TabularInline):
    model = Zettel
    exclude = ('inputs', 'outputs')
    extra = 1


class InputAdmin(admin.ModelAdmin):
    model = Input


class OutputAdmin(admin.ModelAdmin):
    model = Output


class ZettelAdmin(admin.ModelAdmin):
    model = Zettel
    inlines = [
        InputZettelInline, OutputZettelInline
    ]


class OriginAdmin(admin.ModelAdmin):
    model = Origin


class ProfileAdmin(admin.ModelAdmin):
    pass


class ProfileErfassungsAdmin(admin.ModelAdmin):
    search_fields = ['user', 'email', 'lastname', 'firstname']
    list_display = ['__str__', 'firstname', 'lastname', 'email']
    inlines = [
        InputProfileInline, OutputProfileInline
    ]


admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(Origin, OriginAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileErfassung, ProfileErfassungsAdmin)
admin.site.register(Zettel, ZettelAdmin)
