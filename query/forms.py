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

SIGNAL_UNITS = (('Frequency', 'Frequency'),
                ('Voltage', 'Voltage-Pos. Seq'),
                ('Current', 'Current-Pos. Seq'),
                ('ROCOF', 'ROCOF'),
                ('Power-Real', 'Power-Real'),
                ('Power-Reactive', 'Power-Reactive'),
                ('Digital', 'Digital'))

DATE_FORMAT = '%m/%d/%Y'

TIME_FORMAT = '%H:%M'

SIGNALS = (('0x84e0-P-01', '<0x84e0-P-01> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VP'),
           ('0x84e0-P-02', '<0x84e0-P-02> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VA'))


def update_stations():
    station_choices = []
    stations = Station.objects.all()

    for station in stations:
        station_choices.append((station.PMU_Name_Short.__str__(), station.__str__()))

    if not station_choices:
        station_choices.insert(0, ('', ''))

    return station_choices


signal_choices = []


def add_signal_choices(signal_objects):
    for signal in signal_objects:
        signal_choices.append((signal.Signal_ID, signal.__str__()))


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

    stations = forms.CharField(required=False,
                               widget=forms.SelectMultiple(
                                   attrs={'size': '3'}, choices=update_stations()))

    condition_type = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField(required=False)

    signal_units = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=SIGNAL_UNITS))

    file = forms.FileField(required=False)


class ConditionForm(forms.Form):
    condition_type = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_TYPES))
    condition_operator = forms.CharField(required=False, widget=forms.Select(choices=CONDITION_OPERATORS))
    condition_value = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 70px;'}))


class SignalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SignalForm, self).__init__(*args, **kwargs)
        global signal_choices
        if not signal_choices:
            signal_choices.insert(0, ('', ''))
        self.fields['signals'] = forms.CharField(
            widget=forms.SelectMultiple(
                attrs={'size': '3'},
                choices=signal_choices))

    @staticmethod
    def update_signals(stations, conditions, signal_units):
        station_pmu_ids = []
        for station in stations:
            station_pmu_ids.append(station.PMU_ID)

        signal_querysets = []
        if stations and not signal_units and not conditions:
            signal_querysets.append(Signal.objects.filter(Signal_PMU_ID__in=station_pmu_ids))
        elif signal_units and not stations and not conditions:
            signal_querysets.append(Signal.objects.filter(Signal_Unit__in=signal_units))
        elif stations and signal_units and not conditions:

            signal_querysets.append(Signal.objects.filter(Signal_PMU_ID__in=station_pmu_ids,
                                                       Signal_Unit__in=signal_units))
        elif conditions:
            for condition in conditions:
                condition_type = condition.condition_type
                condition_operator = condition.condition_operator
                condition_value = condition.condition_value
                if condition_type == "voltage":
                    if condition_operator == "=":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))
                    elif condition_operator == "!=":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage__lte=condition_value,
                                                                      Signal_Voltage__gte=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))
                    elif condition_operator == "<":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage__lt=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))
                    elif condition_operator == "<=":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage__lte=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))
                    elif condition_operator == ">":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage__gt=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))
                    elif condition_operator == ">=":
                        signal_querysets.append(Signal.objects.filter(Signal_Voltage__gte=condition_value,
                                                                      Signal_PMU_ID__in=station_pmu_ids,
                                                                      Signal_Unit__in=signal_units))

        global signal_choices
        signal_choices = []

        for signal_queryset in signal_querysets:
            add_signal_choices(signal_queryset)

        # No specific signals were filtered, list them all
        if not signal_querysets:
            signal_objects = Signal.objects.all()
            add_signal_choices(signal_objects)

        # No signals made it through the filter so list nothing
        if not signal_choices:
            signal_choices.insert(0, ('', ''))

        print(signal_choices)