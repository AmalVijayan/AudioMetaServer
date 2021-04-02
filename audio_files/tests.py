from django.test import TestCase
from django.utils import timezone
import datetime 
from .models import validate_datetime
from django.core.exceptions import ValidationError


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
