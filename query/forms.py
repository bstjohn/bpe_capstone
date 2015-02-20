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
                ('Digital', 'Digital'),
                ('Analog', 'Analog'),
                ('Frequency', 'Frequency'))

ASSET_CHOICES = (('Bus', 'Bus'),
                 ('Line', 'Line'),
                 ('Transformer', 'Transformer'),
                 ('Generator', 'Generator'),
                 ('Capacitor', 'Capacitor'),
                 ('Reactor', 'Reactor'),
                 ('Digital', 'Digital'),
                 ('Analog', 'Analog'))

UNIT_CHOICES = (('Voltage', 'Voltage'),
                ('Current', 'Current'),
                ('Digital', 'Digital'),
                ('Power-Real', 'Power-Real'),
                ('Power-Reactive', 'Power-Reactive'),
                ('Frequency', 'Frequency'),
                ('ROCOF', 'ROCOF'))

PHASE_CHOICES = (('Pos. Seq', 'Pos. Seq'),
                 ('Phase A', 'Phase A'),
                 ('Phase B', 'Phase B'),
                 ('Phase C', 'Phace C'),
                 ('Zero Seq', 'Zero Seq'),
                 ('Neg. Seq', 'Neq. Seq'))

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

        convert_to_int(station_voltage)

        kwargs = {}
        add_kwarg(kwargs, 'PMU_Voltage', station_voltage, Station)
        add_kwarg(kwargs, 'PMU_Channel', pmu_channel, Station)

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
        global signal_choices
        signal_choices = []
        station_pmu_ids = []
        for station in stations:
            station_pmu_ids.append(station.PMU_ID)

        signal_voltage = convert_to_int(signal_voltage)

        kwargs = {}
        add_kwarg(kwargs, 'Signal_PMU_ID', station_pmu_ids, Signal)
        add_kwarg(kwargs, 'Signal_Voltage', signal_voltage, Signal)
        add_kwarg(kwargs, 'Signal_Type', signal_type, Signal)
        add_kwarg(kwargs, 'Signal_Asset', signal_asset, Signal)
        add_kwarg(kwargs, 'Signal_Unit', signal_unit, Signal)
        add_kwarg(kwargs, 'Signal_Phase', signal_phase, Signal)
        print(kwargs)
        
        signal_query_object = Signal.objects.filter(**kwargs)

        add_signal_choices(signal_query_object)

        # Ass all signals to list if no filter parameters
        if not signal_query_object \
                and not stations and not signal_voltage \
                and not signal_type and not signal_asset\
                and not signal_unit and not signal_phase:
            add_signal_choices(Signal.objects.all())

        # No signals made it through the filter so list nothing
        if not signal_choices:
            signal_choices.insert(0, ('', ''))


def add_kwarg(kwargs, field, values, model):
    kwargs['{0}__{1}'.format(field, 'in')] = values if values else model.objects.all().values_list(field, flat=True)


def convert_to_int(string_list):
    for i, string_object in enumerate(string_list):
        print(string_object)
        string_list[i] = int(string_object)
        
    return string_list