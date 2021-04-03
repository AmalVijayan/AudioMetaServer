from django.test import TestCase
from django.utils import timezone
import datetime 
from .models import validate_datetime, validate_participants
from django.core.exceptions import ValidationError
from random import randint

# Create your tests here.

print("\n\n ++++++++++++++++++++++++++++++++ Initiating Model Test ++++++++++++++++++++++++++++++++++++++++ \n\n")


class SongTests(TestCase):

    #Validating datetime field
    print("testing datetime validation ...")

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
        uploadedtime fails validation if it is a past datetime
        """
        with self.assertRaises(ValidationError):
            validate_datetime(timezone.now()-datetime.timedelta(seconds=3))



class PodcastTests(TestCase):

    #Validating participants field
    print("testing participants validation ...")

    # Positive test case 
    def test_participants_does_not_exceed(self):
        """
        Participants succeeds validation if it is contains less than 10 names
        """

        try:
            validate_participants(str([str(randint(10000, 900000)) for i in range(10)]))
        except:
            self.assertRaises(ValidationError)

    def test_participant_name_does_not_exceed(self):
        """
        Participants succeeds validation if it is contain names less than 100 characters long
        """
        try:
            validate_participants(str([str(randint(10000, 900000)) for i in range(10)]))
        except:
            self.assertRaises(ValidationError)
            
    # Negative  test cases
    def test_participants_exceeds(self):
        """
        Participants fails validation if it is contains more than 10 names
        """
        with self.assertRaises(ValidationError):
            validate_participants(str([str(randint(10000, 900000)) for i in range(12)]))

    def test_participant_name_exceeds(self):
        """
        Participants fails validation if it is contain names longer than 100 chars
        """
        with self.assertRaises(ValidationError):
            validate_participants(str(['93fbec92b2c409188e241789535fbb3147c98f314ea5ed1870cac55c37c1cc4b3fa3841f96dace38c1d45b325af473118d0fd985d35114b4b09']))