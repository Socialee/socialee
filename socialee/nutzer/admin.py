from django.contrib import admin
from django.contrib.contenttypes import generic

# Register your models here.
from .models import Input, Output, Profile


class InputInline(admin.TabularInline):
	model = Input


class OutputInline(admin.TabularInline):
	model = Output


class InputAdmin(admin.ModelAdmin):
	model = Input


class OutputAdmin(admin.ModelAdmin):
	model = Output


class ProfileAdmin(admin.ModelAdmin):
	# search_fields = ['user','email','lastname', 'firstname']
	# list_display = ['__unicode__', 'firstname', 'lastname', 'updated', 'timestamp']
	inlines = [
		InputInline, OutputInline,
	]


admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(Profile, ProfileAdmin)
