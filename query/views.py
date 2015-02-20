from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError

from query.forms import QueryForm, StationForm, StationFilterForm, SignalForm, SignalFilterForm
from query.models import Query, SystemStatus, SystemNode, SystemCpu
from stations.models import Station

import datetime
import time
import json


class Condition:
    def __init__(self, condition_type, condition_operator, condition_value):
        self.condition_type = condition_type
        self.condition_operator = condition_operator
        self.condition_value = condition_value

    def __str__(self):
        return self.condition_type + " " + self.condition_operator + " " + str(self.condition_value)


class QueryObject:
    def __init__(self, model_id, start_date_time, end_date_time,
                 conditions, file_name, signals, qr_file,
                 ar_file, status_field, sr_completed):
        self.model_id = model_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.conditions = conditions
        self.file_name = file_name
        self.signals = signals
        self.qr_file = qr_file
        self.ar_file = ar_file
        self.sr_completed = sr_completed
        self.status_field = status_field


class SystemStatusObject:
    def __init__(self, system_id):
        self.system_id = system_id


class SystemNodeObject:
    def __init__(self, node_id, used, available):
        self.node_id = node_id
        self.used = used
        self.available = available


class SystemCpuObject:
    def __init__(self, cpu_id, cpu_load):
        self.cpu_id = cpu_id
        self.cpu_load = cpu_load


@login_required
def query_index(request):
    return render(request, 'query/query.html')


@login_required
def query_result(request):
    return render(request, 'query/query-result.html')


@login_required
def status_result(request):
    return render(request, 'query/status-result.html')


current_step = 0
stations = ''
query_model = Query()
ss_model = SystemStatus()
query_object = QueryObject(None, None, None, None, None, None, None, None, None, None)
ss_object = SystemStatusObject(None)
sn_object = SystemNodeObject(None, None, None)
scpu_object = SystemCpuObject(None, None)


# calculate and return a results page render
# - pass in a request and query model,
# - and return the rendered page 
@login_required
def return_result_page(request, query_model):
    context = {
        'query_id': query_model.id,
        'qr_file': query_model.qr_file,
        'ar_file': query_model.ar_file,
        'status_field': query_model.status_field,
        'sr_completed': query_model.sr_completed}
    return render(request, 'query/query-result.html', context)


# System Status
# calculate and return the rendered page
def return_status_page(request, StatusResponse):
    context = {
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        #     calculate what needs to be passed in
        #  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    }
    return render(request, 'query/query-result.html', context)


def get_context(username, form, station_form, station_filter_form, signal_form,
                signal_filter_form, step):
    return {'username': username, 'form': form, 'station_form': station_form,
            'station_filter_form': station_filter_form, 'signal_form': signal_form,
            'signal_filter_form': signal_filter_form, 'current_step': step}


# Builds a query given user input
@login_required
def query_builder(request):
    global query_model
    global query_object
    global current_step
    global stations

    username = None
    if request.user.is_authenticated():
        username = request.user.username
        query_model.user_name = username
        creation_date = time.strftime("%Y-%m-%d %H:%M:%S")
        query_model.create_date_time = creation_date

    if not request.method == 'POST':
        detail_form = QueryForm()
        station_form = StationForm()
        station_filter_form = StationFilterForm(initial=StationFilterForm.get_initial_station_values())
        signal_form = SignalForm()
        signal_filter_form = SignalFilterForm(initial=SignalFilterForm.get_initial_signal_values())

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)

    detail_form = QueryForm(request.POST, request.FILES)
    signal_form = SignalForm(request.POST)
    signal_filter_form = SignalFilterForm(
        request.POST,
        initial=SignalFilterForm.get_initial_signal_values())
    station_form = StationForm(request.POST)
    station_filter_form = StationFilterForm(
        request.POST, 
        initial=StationFilterForm.get_initial_station_values())
    if detail_form.is_valid() and 'save-details' in request.POST:
        signal_form = SignalForm()
        current_step = 1

        query_model.owner = request.user
        query_model.query_name = detail_form.cleaned_data['query_name']
        start_date = detail_form.cleaned_data['start_date']
        start_time = detail_form.cleaned_data['start_time']
        start_date_time = datetime.datetime.combine(start_date, start_time)
        query_model.start_date_time = start_date_time
        end_date = detail_form.cleaned_data['end_date']
        end_time = detail_form.cleaned_data['end_time']
        end_date_time = datetime.datetime.combine(end_date, end_time)
        query_model.end_date_time = end_date_time

        try:
            file = request.FILES["file"]
            file_name = file.name
        except MultiValueDictKeyError:
            file_name = ""
        query_model.file_name = file_name

        query_object = QueryObject(None, start_date_time, end_date_time,
                                   None, file_name, None, None, None, None, None)

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif not detail_form.is_valid() and 'save-details' in request.POST:
        signal_form = SignalForm()
        current_step = 0
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif 'save-details' in request.POST:
        signal_form = SignalForm()
        current_step = 1
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif station_filter_form.is_valid() and 'station-filter-submit' in request.POST:
        detail_form = QueryForm()
        signal_form = SignalForm()
        current_step = 2

        # station_voltage = station_filter_form.cleaned_data['station_voltage']
        station_voltage = request.POST.getlist('station_voltage')
        pmu_channel = request.POST.getlist('pmu_channel')
        StationForm.update_stations(station_form, station_voltage, pmu_channel)
        station_form = StationForm()

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif 'station-filter-submit' in request.POST:
        detail_form = QueryForm()
        signal_form = SignalForm()
        current_step = 2

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif station_form.is_valid() and 'station-submit' in request.POST:
        detail_form = QueryForm()
        current_step = 3

        stations = request.POST.getlist('stations')
        query_model.set_stations(stations)

        station_objects = get_stations(stations)

        signal_form.update_signals(station_objects, [], [], [], [], [])
        
        signal_form = SignalForm()

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif 'station-submit' in request.POST:
        detail_form = QueryForm()
        signal_form = SignalForm()

        current_step = 3
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif signal_filter_form.is_valid() and 'signal-filter-submit' in request.POST:
        detail_form = QueryForm()
        current_step = 4

        signal_voltage = request.POST.getlist('signal_voltage')
        signal_type = request.POST.getlist('signal_type')
        signal_asset = request.POST.getlist('signal_asset')
        signal_unit = request.POST.getlist('signal_unit')
        signal_phase = request.POST.getlist('signal_phase')

        station_objects = get_stations(stations)

        signal_form.update_signals(station_objects, signal_voltage, signal_type,
                                  signal_asset, signal_unit, signal_phase)
                                  
        signal_form = SignalForm()
                                  

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif 'signal-filter-form' in request.POST:
        detail_form = QueryForm()
        signal_form = SignalForm()

        current_step = 4
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif signal_form.is_valid() and 'send' in request.POST:
        query_model.save()
        query_object.model_id = query_model.id
        query_object.signals = request.POST.getlist('signals')
        print(convert_to_json(query_object))

        return return_result_page(request, query_model)
    elif 'send' in request.POST:
        detail_form = QueryForm()
        current_step = 4
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)


def get_stations(station_list):
    station_objects = []
    for station in station_list:
        station_queryset = Station.objects.filter(PMU_Name_Short=station)
        station_objects = get_query_objects(station_queryset, station_objects)
    return station_objects


def get_query_objects(query_set, query_object_list):
    for station_object in query_set:
        query_object_list.append(station_object)
    return query_object_list


def convert_to_json(query_param):
    query_id = query_param.model_id
    start_date_time = query_param.start_date_time
    end_date_time = query_param.end_date_time
    file_name = query_param.file_name
    signals = query_param.signals

    query = json.dumps({
        "query": {
            "query_id": query_id,
            "start": start_date_time.__str__(),
            "end": end_date_time.__str__(),
            "analysis_file": file_name,
            "signal_id": signals
        }
    })

    return query
