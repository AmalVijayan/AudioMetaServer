from rest_framework import serializers
import audio_files.models
from django.conf import settings


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = audio_files.models.Song
        fields = '__all__'
