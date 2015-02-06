from django import forms
from django.forms.widgets import TimeInput, DateInput


STATION_CHOICES = (('0x84e1', '[ALBN-500-B1-SA] [0x84e1]       Albion           500V 1 SA-B'),
                   ('0x8547', '[ALCN-500-B1-SA] [0x8547]       Alicante         500V 1 SA-B'),
                   ('0x852b', '[ASSS-500-B1-SA] [0x852b]       Assisi           500V 1 SA-B'),
                   ('station4', 'Station4'),
                   ('station5', 'Station5'))

CONDITION_TYPES = (('voltage', 'Voltage'),
                   ('current', 'Current'),
                   ('frequency', 'Frequency'))

CONDITION_OPERATORS = (('==', '=='),
                       ('!=', '!='),
                       ('<', '<'),
                       ('<=', '<='),
                       ('>', '>'),
                       ('>=', '>='))

DATE_FORMAT = '%m/%d/%Y'

TIME_FORMAT = '%H:%M'


# The query form attributes
class QueryForm(forms.Form):
    query_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    start_date = forms.DateField(widget=DateInput(attrs={'placeholder': 'mm/dd/yyyy',
                                                         'class': 'datepicker'},
                                                  format=DATE_FORMAT))
    start_time = forms.TimeField(widget=TimeInput(attrs={'placeholder': 'HH:MM:SS (24-hour)'},
                                                  format=TIME_FORMAT))

    end_date = forms.DateField(widget=DateInput(attrs={'placeholder': 'mm/dd/yyyy',
                                                       'class': 'datepicker'},
                                                format=DATE_FORMAT))
    end_time = forms.TimeField(widget=TimeInput(attrs={'placeholder': 'HH:MM:SS (24-hour)'},
                                                format=TIME_FORMAT))

    stations = forms.CharField(widget=forms.SelectMultiple(attrs={'size': '3'}, choices=STATION_CHOICES))

    condition_type = forms.CharField(widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField()

    file = forms.FileField()


class ConditionForm(forms.Form):
    condition_type = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 70px;'}))