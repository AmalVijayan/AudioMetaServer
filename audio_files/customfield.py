from django.db import models
import re
from django.core.exceptions import ValidationError

def parse_list(hand_string):
    """Takes a string of comma seperated values and splits them."""
    rex = re.compile('(.+?)(?:,|$)')
    args = [x.strip() for x in rex.findall(hand_string)]
    # print(" - ------------ - -----------------")
    # print(args)
    # if len(args) > 10:
    #     raise ValidationError("There can not be more than 10 participants")
    return args

class CommaSeparatedValuesField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(CommaSeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)
     
    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return value
        return parse_list(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
    
   