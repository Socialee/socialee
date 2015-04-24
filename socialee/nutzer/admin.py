from django.contrib import admin
from django.contrib.contenttypes import generic

# Register your models here.
from .models import User, Digiinput, Digioutput

class DigiinputInline(admin.TabularInline):
	model = Digiinput
	date_hierarchy = 'timestamp'
	search_fields = ['bietet']
	list_display = ['__unicode__', 'updated', 'timestamp']
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = User

class DigioutputInline(admin.TabularInline):
	model = Digioutput
	date_hierarchy = 'timestamp'
	search_fields = ['braucht']
	list_display = ['__unicode__', 'updated', 'timestamp']
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = User

class DigiinputAdmin(admin.ModelAdmin):
	model = Digiinput
	date_hierarchy = 'timestamp'
	search_fields = ['bietet']
	list_display = ['__unicode__', 'updated', 'timestamp']
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = User

class DigioutputAdmin(admin.ModelAdmin):
	model = Digioutput
	date_hierarchy = 'timestamp'
	search_fields = ['braucht']
	list_display = ['__unicode__', 'updated', 'timestamp']
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = User


class UserAdmin(admin.ModelAdmin):

	date_hierarchy = 'timestamp'
	search_fields = ['user','email','lastname', 'firstname']
	list_display = ['__unicode__', 'firstname', 'lastname', 'updated', 'timestamp']
	inlines = [
		DigiinputInline, DigioutputInline,
	]
	#list_editable = ['active']
	#list_filter = ['user', 'active']
	readonly_fields = ['updated', 'timestamp']
	#prepopulated_fields = {"slug":("user",)}
	class Meta:
		model = User





admin.site.register(User, UserAdmin)

admin.site.register(Digiinput, DigiinputAdmin)
admin.site.register(Digioutput, DigioutputAdmin)