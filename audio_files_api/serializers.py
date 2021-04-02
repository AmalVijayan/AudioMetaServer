from rest_framework import serializers
import audio_files.models
from django.conf import settings


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = audio_files.models.Song
        # fields = '__all__'
        fields = ('id',
                  'name',
                  'duration',
                  'uploadedtime'
                 )

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = audio_files.models.Podcast
        fields = '__all__'

class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = audio_files.models.AudioBook
        fields = '__all__'

