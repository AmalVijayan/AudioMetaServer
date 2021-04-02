from django.contrib import admin
from .models import Song, Podcast

# Register your models here.

class SongAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime',)

class PodcastAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime', 'host', 'participants', )

admin.site.register(Song, SongAdmin)
admin.site.register(Podcast, PodcastAdmin)
