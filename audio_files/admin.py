from django.contrib import admin
from .models import Song, Podcast, AudioBook

# Register your models here.

class SongAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime',)

class PodcastAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime', 'host', 'participants', )

class AudioBookAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime', 'author', 'narrator', )

admin.site.register(Song, SongAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(AudioBook, AudioBookAdmin)
