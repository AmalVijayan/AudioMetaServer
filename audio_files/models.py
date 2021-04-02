
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime 
from .customfield import CommaSeparatedValuesField
import re

# A filed validater for determinig if the date entered is a future date or not (Only allows future dates)
def validate_datetime(value):
    if value < ( timezone.now() - datetime.timedelta(seconds=2) ) : # Compensating 2 seconds for network or user-action latency
        raise ValidationError("The date & time cannot be in the past!")
    return value


def validate_participants(value):
    """Takes a string of comma seperated values and splits them."""
    list_exceeds_10 = len(value) - 10
    if list_exceeds_10 > 0 :
        raise ValidationError(f"There can not be more than 10 participants! Please remove {list_exceeds_10} participants")
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
        return f"SONG - {self.name}"


class Podcast(Attributes):
    host = models.CharField(max_length=100, blank=False, null=False)
    participants = CommaSeparatedValuesField(blank=True, null=True, validators=[validate_participants])

    def __str__(self):
        return f"PODCAST - {self.name}"


class AudioBook(Attributes):
    author = models.CharField(max_length=100, blank=False, null=False)
    narrator = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"AUDIOBOOK - {self.name}"