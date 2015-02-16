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

PMU_CHANNEL_CHOICES = (('A', 'A'),
                       ('B', 'B'))

TYPE_CHOICES = (('Phasor', 'Phasor'),
                ('Analog', 'Analog'),
                ('Digital', 'Digital'),
                ('Frequency', 'Frequency'))

ASSET_CHOICES = (('Bus', 'Bus'),
                 ('Line', 'Line'),
                 ('Transformer', 'Transformer'),
                 ('Generator', 'Generator'),
                 ('Capacator', 'Capacator'),
                 ('Reactor', 'Reactor'),
                 ('Digital', 'Digital'),
                 ('Analog', 'Analog'))

UNIT_CHOICES = (('ROCOF', 'ROCOF'),
                ('Frequency', 'Frequency'),
                ('Power-Reactive', 'Power-Reactive'),
                ('Power-Real', 'Power-Real'),
                ('Current', 'Current-Pos. Seq'),
                ('Voltage', 'Voltage-Pos. Seq'))

PHASE_CHOICES = (('Phase A', 'Phase A'),
                 ('Phase B', 'Phase B'),
                 ('Phase C', 'Phace C'),
                 ('Zero Seq', 'Zero Seq'),
                 ('Neg. Seq', 'Pos. Seq'))

DATE_FORMAT = '%m/%d/%Y'

TIME_FORMAT = '%H:%M'

SIGNALS = (('0x84e0-P-01', '<0x84e0-P-01> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VP'),
           ('0x84e0-P-02', '<0x84e0-P-02> Phasor  Bus #1     N         Voltage-Pos. Seq    B500NORTH____1VA'))

VOLTAGE_CHOICES = (('230', '230'),
                   ('500', '500'))


signal_choices = []
station_choices = []


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

    file = forms.FileField(required=False)


class StationFilterForm(forms.Form):
    station_voltage = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=VOLTAGE_CHOICES))
    pmu_channel = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=PMU_CHANNEL_CHOICES))


class StationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StationForm, self).__init__(*args, **kwargs)
        global station_choices
        if not station_choices:
            station_choices.insert(0, ('', ''))
        self.fields['stations'] = forms.CharField(
            widget=forms.SelectMultiple(
                attrs={'size': '3'},
                # choices=station_choices))
                choices=station_choices))

    @staticmethod
    def update_stations(station_voltage, pmu_channel):
        global station_choices
        station_choices = []
        stations = Station.objects.all()

        for station in stations:
            station_choices.append((station.PMU_Name_Short.__str__(), station.__str__()))

        if not station_choices:
            station_choices.insert(0, ('', ''))

        return station_choices



class SignalFilterForm(forms.Form):
        signal_voltage = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=VOLTAGE_CHOICES))
        signal_type = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=TYPE_CHOICES))
        signal_asset = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=ASSET_CHOICES))
        signal_unit = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=UNIT_CHOICES))
        signal_phase = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=PHASE_CHOICES))


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
    def update_signals(stations, signal_voltage, signal_type,
                       signal_asset, signal_unit, signal_phase):
        station_pmu_ids = []
        for station in stations:
            station_pmu_ids.append(station.PMU_ID)

        signal_querysets = [
            Signal.objects.filter(Signal_PMU_ID__in=station_pmu_ids),
            Signal.objects.filter(Signal_Voltage__in=signal_voltage),
            Signal.objects.filter(Signal_Type__in=signal_type),
            Signal.objects.filter(Signal_Asset__in=signal_asset),
            Signal.objects.filter(Signal_Unit__in=signal_unit),
            Signal.objects.filter(Signal_Phase__in=signal_phase),
        ]

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