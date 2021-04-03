from django.test import TestCase
from django.utils import timezone
import datetime 
from .models import validate_datetime, validate_participants
from django.core.exceptions import ValidationError
from random import randint

# Create your tests here.


class SongTests(TestCase):

    #Validating datetime field

    # Positive test case 
     def test_future_datetime(self):
        """
        uploadedtime succeeds validation if it is a future datetime
        """
        try:
            validate_datetime(timezone.now()+datetime.timedelta(seconds=3))
        except ExceptionType:
            self.assertRaises(ValidationError)
            

    # Negative  test cases
     def test_past_datetime(self):
        """
        name succeeds validation if it is a str
        """
        with self.assertRaises(ValidationError):
            validate_datetime(timezone.now()-datetime.timedelta(seconds=3))



# class PodcastTests(TestCase):

#     #Validating datetime field

#     # Positive test case 
#      def test_participants_does_not_exceed(self):
#         """
#         Participants succeeds validation if it is contains less than 10 names
#         """
#         try:
#             validate_participants([str(randint(10000, 900000)) for i in range(11)])
#         except:
#             self.assertRaises(ValidationError)
            

#     # Negative  test cases
#      def test_participants_exceeds(self):
#         """
#         Participants fails validation if it is contains more than 10 names
#         """
#         with self.assertRaises(ValidationError):
#             validate_participants([str(randint(10000, 900000)) for i in range(12)])