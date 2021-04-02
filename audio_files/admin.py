from django.contrib import admin
from .models import Song

# Register your models here.

class SongAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'uploadedtime', )
    list_display = ('__str__', 'id', 'name', 'duration', 'uploadedtime',)

admin.site.register(Song, SongAdmin)
