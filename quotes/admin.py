from django.contrib import admin
from .models import Quote

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(active=True)
make_published.short_description = "Alle markierten Zitate veröffentlichen."

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'active')
    list_editable = ['active']
    actions = [make_published]

admin.site.register(Quote, QuoteAdmin)