import os
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
import json
import audio_files.models
import pandas as pd
import datetime 
from random import randint

# Create your tests here.

print("\n\n ++++++++++++++++++++++++++++++++ Initiating API Test ++++++++++++++++++++++++++++++++++++++++\n\n")


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

    def test_delete_song(self):
        """
        This test ensures that we can delete a song object
        """

        print("\n Testing delete_song ...")

        song1 = audio_files.models.Song.objects.create(name="Micheal Jackson | Beat-it",
                                                        duration=230,
                                                        uploadedtime=timezone.now())            
        url = f"/song/{song1.id}/"
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204,
            msg={'url': url, 'response': response}
        )



class AudioBookTest(APITestCase):

    def test_create_or_upload_audiobooks(self):
        """
        This test ensures that we can create or upload audiobooks
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Audiobook' : 'audiobook', 'Not None' : 'The Psychology of Money', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/AUDIOBOOK_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'create_audiobook']


        print("\n Testing create_audiobook ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):
                # Pre-cleanup 
                audio_files.models.AudioBook.objects.all().delete()
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
                        "uploadedtime": str(uploadedtime),
                        "author": mapping[row['author']],
                        "narrator": mapping[row['narrator']]
                        }
                    }

                url = reverse('audio_file_create')

                response = self.client.post(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')

                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_retrieve_audiobook(self):
        """
        This test ensures that we can retrieve the details of a particular audiobook
        """
        print("\n Testing retrieve_audiobook ...")

        ab = audio_files.models.AudioBook.objects.create(name="The Psychology of Money",
                                                        duration=10444,
                                                        uploadedtime=timezone.now(),
                                                        author="Jonny Ranne",
                                                        narrator="Simpson J")     
         
        url = f"/audiobook/{ab.id}/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )

    def test_list_audiobooks(self):
        """
        This test ensures that we can list all audiobooks
        """
        print("\n Testing list_audiobook ...")

        ab1 = audio_files.models.AudioBook.objects.create(name="The Psychology of Money",
                                                         duration=10444,
                                                         uploadedtime=timezone.now(),
                                                         author="Jonny Ranne",
                                                         narrator="Simpson J")    

        ab2 = audio_files.models.AudioBook.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        author="Mark Manson",
                                                        narrator="Roger Wayne")             
        url = f"/audiobook/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )

    def test_update_audiobook(self):
        """
        This test ensures that we can update an existing audiobook object
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Audiobook' : 'audiobook', 'Not None' : 'The Psychology of Money', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/AUDIOBOOK_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'update_audiobook']

        print("\n Testing update_audiobook ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):

                # Pre-cleanup
                audio_files.models.AudioBook.objects.all().delete()

                ab = audio_files.models.AudioBook.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        author="Mark Manson",
                                                        narrator="Roger Wayne")        

                if row['uploadedtime'].lower() == 'now':
                    uploadedtime = timezone.now()
                else:
                    uploadedtime = timezone.now() - datetime.timedelta(seconds=50)

                payload = {
                    "audioFileType": mapping[row['audioFileType'].title()],
                    "audioFileMetadata": {
                        "name": mapping[row['name']], 
                        "duration": row['duration'],
                        "uploadedtime": str(uploadedtime),
                        "author": mapping[row['author']],
                        "narrator": mapping[row['narrator']]
                        }
                }
                url = f"/audiobook/{ab.id}/"

                response = self.client.put(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')
                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_delete_audiobook(self):
        """
        This test ensures that we can delete a song object
        """

        print("\n Testing delete_audiobook ...")

        ab = audio_files.models.AudioBook.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        author="Mark Manson",
                                                        narrator="Roger Wayne")           
        url = f"/audiobook/{ab.id}/"
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204,
            msg={'url': url, 'response': response}
        )
    


class PodcastTest(APITestCase):

    def test_create_or_upload_podcasts(self):
        """
        This test ensures that we can create or upload podcasts
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Podcast' : 'podcast', 'Not None' : 'The Mindset Mentor', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}

        participants_mapper = {'None': None,  'Not None' : [str(randint(10000, 900000)) for i in range(10)],  '_gt 10' : [str(randint(10000, 900000)) for i in range(12)] }
        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/PODCAST_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'create_podcast']


        print("\n Testing create_podcast ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):
                # Pre-cleanup 
                audio_files.models.Podcast.objects.all().delete()
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
                        "uploadedtime": str(uploadedtime),
                        "host": mapping[row['host']],
                        "participants": participants_mapper[row['participants']]
                        }
                    }

                url = reverse('audio_file_create')

                response = self.client.post(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')

                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_retrieve_podcast(self):
        """
        This test ensures that we can retrieve the details of a particular podcast
        """
        print("\n Testing retrieve_podcast ...")

        podcast = audio_files.models.Podcast.objects.create(name="The Mindset Mentor",
                                                        duration=104444,
                                                        uploadedtime=timezone.now(),
                                                        host="Rob Dial and Kast Media",
                                                        participants=str([str(randint(10000, 900000)) for i in range(10)]))     
         
        url = f"/podcast/{podcast.id}/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )

    def test_list_podcasts(self):
        """
        This test ensures that we can list all audiobooks
        """
        print("\n Testing list_podcast ...")

        podcast1 = audio_files.models.Podcast.objects.create(name="The Psychology of Money",
                                                         duration=10444,
                                                         uploadedtime=timezone.now(),
                                                         host="Jonny Ranne",
                                                         participants=str([str(randint(10000, 900000)) for i in range(10)])) 

        podcast2 = audio_files.models.Podcast.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        host="Mark Manson",
                                                        participants=str([str(randint(10000, 900000)) for i in range(10)])) 
        url = f"/podcast/"

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg={'url': url, 'response': response.json()}
        )

    def test_update_podcast(self):
        """
        This test ensures that we can update an existing podcast object
        """
    
        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {'None': None, 'Podcast' : 'podcast', 'Not None' : 'The Psychology of Money', '_gt 100' : '93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09'}
        participants_mapper = {'None': None,  'Not None' : [str(randint(10000, 900000)) for i in range(10)],  '_gt 10' : [str(randint(10000, 900000)) for i in range(12)] }

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv('unittest_data/PODCAST_API_TEST_CASES.csv')
        df_test_cases = df_test_cases[df_test_cases['Method'] == 'update_podcast']

        print("\n Testing update_podcast ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):

                # Pre-cleanup
                audio_files.models.Podcast.objects.all().delete()

                podcast = audio_files.models.Podcast.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        host="Mark Manson")
                                                       # participants=[])               

                if row['uploadedtime'].lower() == 'now':
                    uploadedtime = timezone.now()
                else:
                    uploadedtime = timezone.now() - datetime.timedelta(seconds=50)

                payload = {
                    "audioFileType": mapping[row['audioFileType'].title()],
                    "audioFileMetadata": {
                        "name": mapping[row['name']], 
                        "duration": row['duration'],
                        "uploadedtime": str(uploadedtime),
                        "host": mapping[row['host']],
                        "participants": participants_mapper[row['participants']]
                        }
                }
                url = f"/podcast/{podcast.id}/"

                response = self.client.put(url, headers= {'Content-Type': 'application/json'}, data=payload, format='json')

                self.assertEqual(
                    response.status_code, row['Expected'],
                    msg={'url': url, 'request_payload': payload, 'response': response.json()}
                )

    def test_delete_podcast(self):
        """
        This test ensures that we can delete a podcast object
        """

        print("\n Testing delete_podcast ...")

        podcast = audio_files.models.Podcast.objects.create(name="The Subtle Art of Not Giving a F*ck",
                                                        duration=122230,
                                                        uploadedtime=timezone.now(),
                                                        host="Mark Manson",
                                                        participants=str(["Ajith","Rana","Milimg"]))
        url = f"/podcast/{podcast.id}/"
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204,
            msg={'url': url, 'response': response}
        )