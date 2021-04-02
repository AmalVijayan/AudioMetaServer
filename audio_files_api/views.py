from django.shortcuts import render
from rest_framework import viewsets, generics, serializers
from rest_framework.views import APIView
import audio_files_api.serializers
import json
import audio_files.models
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict

# Create your views here.

class AudioViewSet(viewsets.ModelViewSet):
# class AudioViewSet(APIView):
    
    def get_queryset(self):

        # print("\n\n ------------------- \n\n")
        # print(self.request.body)
        # print(self.request.method)
        # print("\n\n ------------------- \n\n")
    
        print(self.kwargs['audioFileType'])

        # if self.request.method == 'POST':
        #     parsed_data = json.loads(self.request.body)
        #     try:
        #         aud_type = parsed_data['audioFileType'].lower()
        #     except:
        #         raise ValidationError("Required fileds missing!")
        # else:
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
        
        if self.action == 'create' or self.action == 'update':

            print(" ---> ", self.request.data)
            aud_type = self.request.data['audioFileType'].lower()

            if aud_type == 'song':
                return audio_files_api.serializers.SongSerializer

            elif aud_type == 'podcast':
                return audio_files_api.serializers.PodcastSerializer

            elif aud_type == 'audiobook':
                return audio_files_api.serializers.AudioBookSerializer
                    # return audio_files_api.serializers.SongSerializer

        else:
            aud_type =  self.kwargs['audioFileType'].lower()
            
            if aud_type == 'song':
                return audio_files_api.serializers.SongSerializer

            elif aud_type == 'podcast':
                return audio_files_api.serializers.PodcastSerializer

            elif aud_type == 'audiobook':
                return audio_files_api.serializers.AudioBookSerializer

    def create(self, request, *args, **kwargs):
        print("\n\n ---------create---------- \n\n")
        print(request.data['audioFileMetadata'])
        print("\n\n ------------------- \n\n")
        aud_type = request.data['audioFileType'].lower()
        payload = request.data['audioFileMetadata']
        serializer = self.get_serializer(data=payload)
        print(" >> SERIALIZER >> : ",serializer)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        print("instance --> ", instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, pk=None, *args, **kwargs):
        print(f"\n\n ---------Update---------- pk : {pk}\n\n")
        print(request.data['audioFileMetadata'])
        print("\n\n ------------------- \n\n")
        aud_type = request.data['audioFileType'].lower()
        payload = request.data['audioFileMetadata']
        serializer = self.get_serializer(data=payload)
        print(" >> SERIALIZER >> : ",serializer)
        serializer.is_valid(raise_exception=True)
        if aud_type == 'song':
            instance = get_object_or_404(audio_files.models.Song, pk=pk)
        if aud_type == 'podcast':
            instance = get_object_or_404(audio_files.models.Podcast, pk=pk)
        if aud_type == 'audiobook':
            instance = get_object_or_404(audio_files.models.AudioBook, pk=pk)
        updated = serializer.update(instance, serializer.data)
        return Response(model_to_dict(updated), status=status.HTTP_200_OK)