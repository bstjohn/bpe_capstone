from django import forms
from django.forms.widgets import TimeInput, DateInput
from stations.models import Station, Signal


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
                 ('Phase C', 'Phase C'),
                 ('Zero Seq', 'Zero Seq'),
                 ('Neg. Seq', 'Neq. Seq'))

VOLTAGE_CHOICES = (('230', '230'),
                   ('500', '500'))

DATE_FORMAT = '%m/%d/%Y'

TIME_FORMAT = '%H:%M'

signal_choices = []
station_choices = []


def add_signal_choices(signal_objects):
    for signal in signal_objects:
        signal_choices.append((signal.Signal_ID, signal.__str__()))


class QueryForm(forms.Form):
    """The fields for the query detail form."""
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
    """The fields for the station filter form."""
    station_voltage = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=VOLTAGE_CHOICES))
    pmu_channel = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=PMU_CHANNEL_CHOICES))
    
    @staticmethod
    def get_initial_station_values():
        """Returns a list of field values that should be pre-selected."""
        return {'station_voltage': ['230', '500'], 'pmu_channel': ['A']}


class StationForm(forms.Form):
    """The definition of the station form."""
    def __init__(self, *args, **kwargs):
        """Initializes the station form with a list of stations that are dynamically updated."""
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
        """Updates the list of stations available to the user.

        Keyword arguments:
        :param: station_voltage: the voltage attribute specified by the user
        :param: pmu_channel: the PMU channel specified by the user
        """
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
        """Retrieves a list of all the stations in the database."""
        global station_choices
        stations = Station.objects.all()
        for station in stations:
            station_choices.append((station.PMU_Name_Short.__str__(), station.__str__()))
        return station_choices


class SignalFilterForm(forms.Form):
        """Defines the fields for the signal filter form."""
        signal_voltage = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=VOLTAGE_CHOICES))
        signal_type = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=TYPE_CHOICES))
        signal_asset = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=ASSET_CHOICES))
        signal_unit = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=UNIT_CHOICES))
        signal_phase = forms.CharField(required=False, widget=forms.CheckboxSelectMultiple(choices=PHASE_CHOICES))

        @staticmethod
        def get_initial_signal_values():
            """Returns a list of field values that should be pre-selected."""
            return {'signal_voltage': ['500'], 'signal_type': ['Phasor'], 'signal_unit': ['Voltage']}


class SignalForm(forms.Form):
    """The definition of the signal filter form."""
    def __init__(self, *args, **kwargs):
        """Initializes the signal form with a list of signals that are dynamically updated."""
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
        """Updates the list of signals that are available to the user.

        Keyword arguments:
        :param: stations: The list of stations the user specified.
        :param: signal_voltage: The signal voltages the user specified.
        :param: signal_type: The signal types the user specified.
        :param: signal_asset: The signal assets the user specified.
        :param: signal_unit: The signal units the user specified.
        :param: signal_phase: The signal phases the user specified.
        """

        global signal_choices
        signal_choices = []
        station_pmu_ids = []
        for station in stations:
            station_pmu_ids.append(station.PMU_ID)

        signal_voltage = convert_to_int(signal_voltage)

        # Define the kwargs that will used as database filters:
        kwargs = {}
        add_kwarg(kwargs, 'Signal_PMU_ID', station_pmu_ids, Signal)
        add_kwarg(kwargs, 'Signal_Voltage', signal_voltage, Signal)
        add_kwarg(kwargs, 'Signal_Type', signal_type, Signal)
        add_kwarg(kwargs, 'Signal_Asset', signal_asset, Signal)
        add_kwarg(kwargs, 'Signal_Unit', signal_unit, Signal)
        add_kwarg(kwargs, 'Signal_Phase', signal_phase, Signal)

        signal_query_object = Signal.objects.filter(**kwargs)

        add_signal_choices(signal_query_object)

        # Ass all signals to list if no filter parameters:
        if not signal_query_object \
                and not stations and not signal_voltage \
                and not signal_type and not signal_asset\
                and not signal_unit and not signal_phase:
            add_signal_choices(Signal.objects.all())

        # No signals made it through the filter so list nothing:
        if not signal_choices:
            signal_choices.insert(0, ('', ''))


def add_kwarg(kwargs, field, values, model):
    """
    Adds a kwarg to a list of kwargs.

    Keyword arguments:
    :param kwargs: The list of kwargs to add to.
    :param field:  The field to be filtered on.
    :param values: The values selected for the field.
    :param model: The model that will be queried from.
    :return:
    """
    kwargs['{0}__{1}'.format(field, 'in')] = values if values else model.objects.all().values_list(field, flat=True)


def convert_to_int(string_list):
    """
    Converts a list of strings to integers.

    Keyword arguments:
    :param string_list: The list of integers in string form.
    :return: The converted list.
    """
    for i, string_object in enumerate(string_list):
        print(string_object)
        string_list[i] = int(string_object)
        
    return string_list