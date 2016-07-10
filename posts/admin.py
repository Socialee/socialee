from django.contrib import admin
from .models import Post



class PostAdmin(admin.ModelAdmin):
	class Meta:
		model = Post

	# list_editable = ['title']
	list_display = ('title', 'timestamp', 'updated')
	list_display_links = ['title']
	list_filter = ['updated', 'timestamp']
	search_fields = ['title', 'content']



admin.site.register(Post, PostAdmin)