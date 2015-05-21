from django.contrib import admin

from .models import Input, Output, Profile, Zettel


class InputInline(admin.TabularInline):
    model = Input


class OutputInline(admin.TabularInline):
    model = Output


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


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'email', 'lastname', 'firstname']
    list_display = ['__str__', 'firstname', 'lastname', 'email']
    inlines = [
        InputInline, OutputInline, ZettelInline
    ]


admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Zettel, ZettelAdmin)
