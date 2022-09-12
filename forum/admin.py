from django.contrib import admin

# Register your models here.
from forum.models import *


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'theme', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'theme', 'time_create')
    search_fields = ('title', 'content')


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Theme, ThemeAdmin)
