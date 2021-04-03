from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
import audio_files_api.serializers
import audio_files.models
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

# Create your views here.

# Single View that handles Song, Podcast and AudioBook

class AudioViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):

        # Choose queryset based on aud_type [Song/Podcast/Audiobook]
        aud_type =  self.kwargs['audioFileType'].lower()

        if aud_type == 'song':
            return audio_files.models.Song.objects.all()

        elif aud_type == 'podcast':
            return audio_files.models.Podcast.objects.all()

        elif aud_type == 'audiobook':
            return audio_files.models.AudioBook.objects.all()

    def get_serializer_class(self):
        
        # Choose serializer based on aud_type [Song/Podcast/Audiobook] and action or request method
        
        """
        The following statement obtains the aud_type from the user depending on the type of request
        In create and update the request data contains the aud_type, all other request contains aud_type as
        a URL parameter
        """
        if self.action == 'create' or self.action == 'update':
            aud_type = self.request.data['audioFileType'].lower()
        else:
            aud_type =  self.kwargs['audioFileType'].lower()

        # Choosing serializer class based on aud_type

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

    # Overriding the create method of Viewset
    def create(self, request, *args, **kwargs):
        try:
            aud_type = request.data['audioFileType'].lower()
        except Exception as e:
            return Response({"msg":"audioFileType filed required or incorrect! Possible values are song/podcast/audiobook", "error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        payload = request.data['audioFileMetadata']

        """
        Podcast requires custom handling for storing and retrieving from a list (Participants list)
        The following block receives the data from the request, converts the participants list to a string
        and stores it in the text field. It creates and saves the complete Podcast object
        """
        if aud_type == 'podcast':
            participants_list = payload['participants']
            payload['participants'] = str(payload['participants'])            
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            op_serialize = audio_files_api.serializers.PodcastRetrieveSerializer(instance, many=False)
            return Response(op_serialize.data, status=status.HTTP_201_CREATED)

        # Create for Song and AudioBook objects
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    # Overriding the update method of Viewset
    def update(self, request, pk=None, *args, **kwargs):

        try:
            aud_type = request.data['audioFileType'].lower()
        except Exception as e:
            return Response({"msg":"audioFileType filed required or incorrect! Possible values are song/podcast/audiobook", "error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        payload = request.data['audioFileMetadata']

        """
        Podcast requires custom handling for storing and retrieving from a list (Participants list)
        The following block receives the data from the request, converts the participants list to a string
        and stores it in the text field. It updates the complete Podcast object
        """
        if aud_type == 'podcast':
            instance = get_object_or_404(audio_files.models.Podcast, pk=pk)
            participants_list = payload['participants']
            payload['participants'] = str(payload['participants'])            
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            updated = serializer.update(instance, serializer.data)
            return Response(model_to_dict(updated), status=status.HTTP_200_OK)

        # Update for Song and AudioBook objects

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        if aud_type == 'song':
            instance = get_object_or_404(audio_files.models.Song, pk=pk)

        if aud_type == 'audiobook':
            instance = get_object_or_404(audio_files.models.AudioBook, pk=pk)
        updated = serializer.update(instance, serializer.data)
        return Response(model_to_dict(updated), status=status.HTTP_200_OK)