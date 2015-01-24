from django import forms
from django.forms.widgets import SplitDateTimeWidget, SelectMultiple, TimeInput, DateInput


STATION_CHOICES = (('station1', 'Station1'),
                   ('station1', 'Station2'),
                   ('station3', 'Station3'))


# The query form attributes
class QueryForm(forms.Form):
    query_name = forms.CharField(label='Name of Your Query', max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    start_date = forms.DateField(label='Start Date', widget=DateInput(attrs={'placeholder': 'mm/dd/yyyy',
                                                                             'class': 'datepicker'}))
    start_time = forms.TimeField(label='Start Time', widget=TimeInput(attrs={'placeholder': 'HH:mm:ss (24-hour)'}))
    end_date = forms.DateField(label='End Date', widget=DateInput(attrs={'placeholder': 'mm/dd/yyyy',
                                                                         'class': 'datepicker'}))
    end_time = forms.TimeField(label='End Time', widget=TimeInput(attrs={'placeholder': 'HH:mm:ss (24-hour)'}))
    stations = forms.CharField(label='Stations', widget=forms.Select(choices=STATION_CHOICES))
