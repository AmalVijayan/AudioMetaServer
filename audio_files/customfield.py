from django.db import models
import re
from django.core.exceptions import ValidationError
import ast



def parse_list(hand_string):
    """Takes a string of comma seperated values and splits them."""
   
    rex = re.compile('(.+?)(?:,|$)')

    args = [x.strip() for x in rex.findall(hand_string)]
    # print(" - ------------ - -----------------")
    # print(args)
    # if len(args) > 10:
    #     raise ValidationError("There can not be more than 10 participants")
    return args

class StringListField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(StringListField, self).__init__(*args, **kwargs)

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

        print("\n\n\nvalue :: ", type(value))
        print("value :: ", value)
        print("ast.literal_eval(value) :: ", ast.literal_eval(value))
        print("TYPE ast.literal_eval(value) :: ", type(ast.literal_eval(value)))
        print("self.token.join([unicode(s) for s in value]) :: ", self.token.join([str(s) for s in value]))

        if not value: return
        # value = ast.literal_eval(value)
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s) for s in value])

    # def value_to_string(self, obj):
    #     value = self._get_val_from_obj(obj)
    #     return self.get_db_prep_value(value)
        
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


# def parse_list(hand_string):
#     """Takes a string of comma seperated values and splits them."""
#     rex = re.compile('(.+?)(?:,|$)')
#     args = [x.strip() for x in rex.findall(hand_string)]
#     return args

# class StringListField(models.TextField):
    
#     def __init__(self, *args, **kwargs):
#         self.token = kwargs.pop('token', ',')
#         super(StringListField, self).__init__(*args, **kwargs)

#     def to_python(self, value):
#         if not value: return
#         if isinstance(value, list):
#             return value
#         return value.split(self.token)

#     def get_db_prep_value(self, value, connection, prepared=False):
#         print("\n\n\nvalue :: ", type(value))
#         print("value :: ", value)
#         print("ast.literal_eval(value) :: ", ast.literal_eval(value))
#         print("TYPE ast.literal_eval(value) :: ", type(ast.literal_eval(value)))
#         print("self.token.join([unicode(s) for s in value]) :: ", self.token.join([str(s) for s in value]))

#         if not value: return
#         # assert(isinstance(value, list) or isinstance(value, tuple))
#         value = ast.literal_eval(value)
#         return str(list(self.token.join([str(s) for s in value])))

#     def value_to_string(self, obj):
#         value = self._get_val_from_obj(obj)
#         return self.get_db_prep_value(value)


    # def __init__(self, *args, **kwargs):
    #     self.token = kwargs.pop('token', ',')
    #     super(StringListField, self).__init__(*args, **kwargs)

    # def to_python(self, value):
    #     if not value: return
    #     if isinstance(value, list):
    #         return value
    #     return value.split(self.token)
     
    # def from_db_value(self, value, expression, connection, context=None):
    #     if value is None:
    #         return value
    #     return parse_list(value)

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     # if not value: return
    #     # assert(isinstance(value, list) or isinstance(value, tuple))
    #     return self.token.join([str(s) for s in value])

    # # def value_to_string(self, obj):
    # #     value = self._get_val_from_obj(obj)
    # #     return self.get_db_prep_value(value)
        
    # def value_to_string(self, obj):
    #     value = self.value_from_object(obj)
    #     return self.get_prep_value(value)



    # description = "Stores a python list"

    # def __init__(self, *args, **kwargs):
    #     super(StringListField, self).__init__(*args, **kwargs)

    # def to_python(self, value):
    #     if not value:
    #         value = []

    #     if isinstance(value, list):
    #         return value

    #     return ast.literal_eval(value)

    # def get_prep_value(self, value):
    #     if value is None:
    #         return value

    #     return value

    # # def value_to_string(self, obj):
    # #     value = self._get_val_from_obj(obj)
    # #     return self.get_db_prep_value(value)

    # def value_to_string(self, obj):
    #     value = self.value_from_object(obj)
    #     return self.get_prep_value(value)