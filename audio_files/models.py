
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime 

# A filed validater for determinig if the date entered is a future date or not (Only allows future dates)
def validate_datetime(value):
    if value < ( timezone.now() - datetime.timedelta(seconds=2) ) : # Compensating 2 seconds for network or user-action latency
        raise ValidationError("The date & time cannot be in the past!")
    return value


# An abstract base class for defining common reusable fields across tables/models
class Attributes(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    duration = models.PositiveIntegerField(blank=False, null=False)
    uploadedtime = models.DateTimeField(blank=False, null=False, validators=[validate_datetime])

    class Meta:
        abstract=True

class Song(Attributes):

    def __str__(self):
        return f"Song - {self.name}"
