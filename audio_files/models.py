
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime 
import re
import ast


# A filed validater for determinig if the date entered is a future date or not (Only allows future dates)
def validate_datetime(value):
    if value < ( timezone.now() - datetime.timedelta(seconds=2) ) : # Compensating 2 seconds for network or user-action latency
        raise ValidationError("The date & time cannot be in the past!")
    return value
    

gt_100_check = lambda x: len(x) > 100


def validate_participants(value):
    plist = ast.literal_eval(value)
    if plist:
        if len(plist) > 10:
            raise ValidationError(f"Number of participants exceeds 10, remove {len(plist) - 10} participants!")
        char_len_check = list(map(gt_100_check, plist))
        if any(char_len_check):
            raise ValidationError(f"Participant names can not be larger than 100 characters!")
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
    participants = models.TextField(blank=True, null=True, validators=[validate_participants])

    def __str__(self):
        return f"PODCAST - {self.name}"


class AudioBook(Attributes):
    author = models.CharField(max_length=100, blank=False, null=False)
    narrator = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"AUDIOBOOK - {self.name}"