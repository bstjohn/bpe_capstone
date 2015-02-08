from django import forms
from django.forms.widgets import TimeInput, DateInput
from stations.models import Station, Signal


STATION_CHOICES = (('0x84e1', '[ALBN-500-B1-SA] [0x84e1]       Albion           500V 1 SA-B'),
                   ('0x8547', '[ALCN-500-B1-SA] [0x8547]       Alicante         500V 1 SA-B'),
                   ('0x852b', '[ASSS-500-B1-SA] [0x852b]       Assisi           500V 1 SA-B'),
                   ('station4', 'Station4'),
                   ('station5', 'Station5'))

CONDITION_TYPES = (('voltage', 'Voltage'),
                   ('current', 'Current'),
                   ('frequency', 'Frequency'))

CONDITION_OPERATORS = (('=', '='),
                       ('!=', '!='),
                       ('<', '<'),
                       ('<=', '<='),
                       ('>', '>'),
                       ('>=', '>='))

DATE_FORMAT = '%m/%d/%Y'

TIME_FORMAT = '%H:%M'


SIGNALS = (('0x84e0-P-01', '<0x84e0-P-01> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VP'),
           ('0x84e0-P-02', '<0x84e0-P-02> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VA'))


def update_stations():
    # global station_choices
    station_choices = ()
    stations = Station.objects.all()
    for station in stations:
        station_choices += (station.PMU_Name_Short.__str__(), station.__str__())
    return station_choices


# The query form attributes
class QueryForm(forms.Form):
    # station_choices = ()

    # def __init__(self, *args, **kwargs):
    #     super(QueryForm).__init__(*args, **kwargs)
    #     self.update_stations()

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

    stations = forms.CharField(required=False,
                               widget=forms.SelectMultiple(
                                   attrs={'size': '3'}, choices=update_stations()))

    condition_type = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField(required=False)

    file = forms.FileField()


class ConditionForm(forms.Form):
    condition_type = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 70px;'}))


signal_choices = ()


class SignalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        global signal_choices
        super(SignalForm, self).__init__(*args, **kwargs)
        self.fields['signals'] = forms.CharField(
            widget=forms.SelectMultiple(
                attrs={'size': '3'},
                choices=signal_choices))

    # signals = forms.CharField(widget=forms.SelectMultiple(attrs={'size': '3'}, choices=SIGNALS))

    def update_signals(self, stations, conditions):
        global signal_choices

        signals_array = []
        for station in stations:
            signals_array.append(Signal.objects.filter(Signal_PMU_ID=station.PMU_ID))

        for condition in conditions:
            condition_type = condition.condition_type
            condition_operator = condition.condition_operator
            condition_value = condition.condition_value
            if condition_type == "voltage":
                if condition_operator == "=":
                    signals_array.append(Signal.objects.filter(Signal_Voltage=condition_value))
                elif condition_operator == "!=":
                    signals_array.append(Signal.objects.filter(Signal_Voltage__lte=condition_value,
                                                               Signal_Voltage__gte=condition_value))
                elif condition_operator == "<":
                    signals_array.append(Signal.objects.filter(Signal_Voltage__lt=condition_value))
                elif condition_operator == "<=":
                    signals_array.append(Signal.objects.filter(Signal_Voltage__lte=condition_value))
                elif condition_operator == ">":
                    signals_array.append(Signal.objects.filter(Signal_Voltage__gt=condition_value))
                elif condition_operator == ">=":
                    signals_array.append(Signal.objects.filter(Signal_Voltage__gte=condition_value))

        for signal_object in signals_array:
            for signal in signal_object:
                signal_choices += (signal.Signal_ID, signal.__str__())

        if not signals_array:
            signal_objects = Signal.objects.all()
            for signal in signal_objects:
                signal_choices += (signal.Signal_ID, signal.__str__())
