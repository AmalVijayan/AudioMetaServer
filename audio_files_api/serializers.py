from rest_framework import serializers
import audio_files.models
from django.conf import settings
import ast

# Object serializers for model objects 

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

# Custom serializer for Listing and Retrieving Podcast objects
class PodcastRetrieveSerializer(serializers.ModelSerializer):

    participants = serializers.SerializerMethodField('get_pList')

    """
    The following function takes care of displaying the participants in a list
    """
    def get_pList(self, podcast):
        participants_text = podcast.participants
        if participants_text:
            participants_list = ast.literal_eval(podcast.participants)
            return participants_list

    class Meta:
        model = audio_files.models.Podcast
        fields = '__all__'

class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = audio_files.models.AudioBook
        fields = '__all__'

