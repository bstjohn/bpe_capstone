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
            station_choices = self.get_all_stations()
        self.fields['stations'] = forms.CharField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'size': '3'},
                choices=station_choices))

    def update_stations(self, station_voltage, pmu_channel):
        global station_choices
        station_choices = []

        # Convert voltages to integer
        for i, voltage in enumerate(station_voltage):
            station_voltage[i] = int(voltage)

        kwargs = {
            '{0}__{1}'.format('PMU_Voltage', 'in'):
                station_voltage if station_voltage else Station.objects.all().values_list('PMU_Voltage', flat=True),
            '{0}__{1}'.format('PMU_Channel', 'in'):
                pmu_channel if pmu_channel else Station.objects.all().values_list('PMU_Channel', flat=True)
        }

        station_query_object = Station.objects.filter(**kwargs)

        for station in station_query_object:
            station_choices.append((station.PMU_Name_Short.__str__(), station.__str__()))

        if not station_choices and not station_voltage and not pmu_channel:
            station_choices = self.get_all_stations()

        if not station_choices:
            station_choices.insert(0, ('', ''))

        return station_choices

    @staticmethod
    def get_all_stations():
        global station_choices
        stations = Station.objects.all()
        for station in stations:
            station_choices.append((station.PMU_Name_Short.__str__(), station.__str__()))
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
            add_signal_choices(Signal.objects.all())
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

        kwargs = {
            '' if not stations else '{0}__{1}'.format('Signal_PMU_ID', 'in'): stations
        }
        signal_query_objects = Signal.objects.filter(**kwargs)
        print(signal_query_objects)

        global signal_choices
        signal_choices = []
        for signal_object in signal_query_objects:
            signal_choices.append(signal_object)

        # No specific signals were filtered, list them all
        if not signal_query_objects and not stations:
            add_signal_choices(Signal.objects.all())

        # No signals made it through the filter so list nothing
        if not signal_choices:
            signal_choices.insert(0, ('', ''))
