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

gt_100_check = lambda x: len(x) > 100

class AudioViewSet(viewsets.ModelViewSet):
# class AudioViewSet(APIView):
    
    def get_queryset(self):

        aud_type =  self.kwargs['audioFileType'].lower()

        if aud_type == 'song':
            return audio_files.models.Song.objects.all()

        elif aud_type == 'podcast':
            return audio_files.models.Podcast.objects.all()

        elif aud_type == 'audiobook':
            return audio_files.models.AudioBook.objects.all()

    def get_serializer_class(self):
        
        if self.action == 'create' or self.action == 'update':
            aud_type = self.request.data['audioFileType'].lower()
        else:
            aud_type =  self.kwargs['audioFileType'].lower()

        if aud_type == 'song':
            return audio_files_api.serializers.SongSerializer

        elif aud_type == 'podcast':
            if self.action == 'list' or self.action == 'retrieve':
                return audio_files_api.serializers.PodcastRetrieveSerializer

            return audio_files_api.serializers.PodcastSerializer

        elif aud_type == 'audiobook':
            return audio_files_api.serializers.AudioBookSerializer
        
        # Default  serializer
        return audio_files_api.serializers.SongSerializer


    def create(self, request, *args, **kwargs):
        try:
            aud_type = request.data['audioFileType'].lower()
        except Exception as e:
            return Response({"msg":"audioFileType filed required or incorrect!", "error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        if aud_type == 'podcast':
            payload = request.data['audioFileMetadata']
            participants_list = payload['participants']
            payload['participants'] = str(payload['participants'])            
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            op_serialize = audio_files_api.serializers.PodcastRetrieveSerializer(instance, many=False)
            return Response(op_serialize.data, status=status.HTTP_201_CREATED)

        payload = request.data['audioFileMetadata']
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, pk=None, *args, **kwargs):
        try:
            aud_type = request.data['audioFileType'].lower()
        except Exception as e:
            return Response({"msg":"audioFileType filed required or incorrect!", "error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        payload = request.data['audioFileMetadata']

        if aud_type == 'podcast':
            instance = get_object_or_404(audio_files.models.Podcast, pk=pk)
            participants_list = payload['participants']
            payload['participants'] = str(payload['participants'])            
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            updated = serializer.update(instance, serializer.data)
            # op_serialize = audio_files_api.serializers.PodcastRetrieveSerializer(instance, many=False)
            return Response(model_to_dict(updated), status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        if aud_type == 'song':
            instance = get_object_or_404(audio_files.models.Song, pk=pk)

        if aud_type == 'audiobook':
            instance = get_object_or_404(audio_files.models.AudioBook, pk=pk)
        updated = serializer.update(instance, serializer.data)
        return Response(model_to_dict(updated), status=status.HTTP_200_OK)