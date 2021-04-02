from django.shortcuts import render
from rest_framework import viewsets, generics, serializers
from rest_framework.views import APIView
import audio_files_api.serializers

import audio_files.models
# Create your views here.

class AudioViewSet(viewsets.ModelViewSet):
# class AudioViewSet(APIView):
    
    def get_queryset(self):

        print("\n\n ------------------- \n\n")
        print(self.request.__dict__)
        print("\n\n ------------------- \n\n")

        print(self.kwargs['audioFileType'])
        """
        Optionally restricts the returned communities to a given Community,
        by filtering against a `slug` query parameter in the URL.
        """
        aud_type =  self.kwargs['audioFileType'].lower()
        if aud_type == 'song':
            print("Its a song")
            queryset = audio_files.models.Song.objects.all()
        elif aud_type == 'podcast':
            print("Its a podcast")
            queryset = audio_files.models.Podcast.objects.all()
        elif aud_type == 'audiobook':
            print("Its an audiobook")
            queryset = audio_files.models.AudioBook.objects.all()
        return queryset

    def get_serializer_class(self):
        aud_type =  self.kwargs['audioFileType'].lower()

        if self.action == 'retrieve':
            if aud_type == 'song':
                return audio_files_api.serializers.SongSerializer
        else:
            return audio_files_api.serializers.SongSerializer
