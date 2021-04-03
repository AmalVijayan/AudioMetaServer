import os
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
import json
import audio_files.models
import pandas as pd
import datetime 


# Base directory for fetchign test data
base_dir = os.path.dirname(os.path.dirname(__file__))

# Create your tests here.


print("\n Initiating API Test")


class SongTest(APITestCase):

    def test_create_or_upload_songs(self):
        """
        This test ensures that we can create or upload songs
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Song' : 'song', 'Not None' : 'Micheal Jackson | BilliJean', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/SONG_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'create_song']


        print("\n Testing create_song ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):
                # Pre-cleanup 
                audio_files.models.Song.objects.all().delete()
                if row['uploadedtime'].lower() == 'now':
                    uploadedtime = timezone.now()
                else:
                    uploadedtime = timezone.now() - datetime.timedelta(seconds=50)

                #preparing payload for testing API
                payload = {
                    "audioFileType": mapping[row['audioFileType'].title()],
                    "audioFileMetadata": {
                        "name": mapping[row['name']], 
                        "duration": row['duration'],
                        "uploadedtime": str(uploadedtime)
                        }
                    }

                url = reverse('audio_file_create')

                response = self.client.post(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')

                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_update_songs(self):
        """
        This test ensures that we can update an existing song object
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Song' : 'song', 'Not None' : 'Micheal Jackson | BilliJean', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/SONG_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'update_song']

        print("\n Testing update_song ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):

                # Pre-cleanup
                audio_files.models.Song.objects.all().delete()

                song = audio_files.models.Song.objects.create(name="Micheal Jackson | Beat-it",
                                                              duration=230,
                                                              uploadedtime=timezone.now())

                if row['uploadedtime'].lower() == 'now':
                    uploadedtime = timezone.now()
                else:
                    uploadedtime = timezone.now() - datetime.timedelta(seconds=50)

                payload = {
                    "audioFileType": mapping[row['audioFileType'].title()],
                    "audioFileMetadata": {
                        "name": mapping[row['name']], 
                        "duration": row['duration'],
                        "uploadedtime": str(uploadedtime)
                        }
                    }
                    
                url = f"/song/{song.id}/"

                response = self.client.put(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')
                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_retrieve_song(self):
        """
        This test ensures that we can retrieve the details of a particular song
        """
        print("\n Testing retrieve_song ...")

        song1 = audio_files.models.Song.objects.create(name="Micheal Jackson | Beat-it",
                                                        duration=230,
                                                        uploadedtime=timezone.now())     
         
        url = f"/song/{song1.id}/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )

    def test_delete_song(self):
        """
        This test ensures that we can delete a song object
        """

        print("\n Testing delete_song ...")

        song1 = audio_files.models.Song.objects.create(name="Micheal Jackson | Beat-it",
                                                        duration=230,
                                                        uploadedtime=timezone.now())            
        url = f"/song/{song1.id}/"
        print("url ::: ", url)
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204,
            msg={'url': url, 'response': response}
        )


    def test_list_song(self):
        """
        This test ensures that we can list all songs
        """
        print("\n Testing list_song ...")

        song1 = audio_files.models.Song.objects.create(name="Micheal Jackson | Beat-it",
                                                        duration=230,
                                                        uploadedtime=timezone.now())   
                                                          
        song2 = audio_files.models.Song.objects.create(name="Micheal Jackson | Billie Jean",
                                                        duration=230,
                                                        uploadedtime=timezone.now())             
        url = f"/song/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )