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


form_submitted = False
current_step = 0
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


# Builds a query given user input
@login_required
def query_builder(request):
    global form_submitted
    global query_model
    global query_object
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        query_model.user_name = username
        creation_date = time.strftime("%Y-%m-%d %H:%M:%S")
        query_model.create_date_time = creation_date

    if not request.method == 'POST':
        form = QueryForm()
        station_form = StationForm()
        station_filter_form = StationFilterForm
        signal_form = SignalForm()
        signal_filter_form = SignalFilterForm()

        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)

    form = QueryForm(request.POST, request.FILES)
    signal_form = SignalForm(request.POST)
    signal_filter_form = SignalFilterForm(request.POST)
    station_form = StationForm(request.POST)
    station_filter_form = StationFilterForm(request.POST)
    if form.is_valid():
        global current_step
        current_step += 1
        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)
    elif station_filter_form.is_valid():
        current_step += 1
        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)
    elif station_form.is_valid():
        current_step += 1
        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)
    elif signal_filter_form.is_valid():
        current_step += 1
        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)
    elif signal_form.is_valid():
        current_step = 0
        context = {'username': username, 'form': form, 'station_form': station_form,
                   'station_filter_form': station_filter_form, 'signal_form': signal_form,
                   'signal_filter_form': signal_filter_form, 'signals_refreshed': int(form_submitted),
                   'current_step': current_step}
        return render(request, 'query/query-builder.html', context)


def get_query_objects(query_set, query_object_list):
    for station_object in query_set:
        query_object_list.append(station_object)
    return query_object_list


def convert_to_json(query_param):
    query_id = query_param.model_id
    start_date_time = query_param.start_date_time
    end_date_time = query_param.end_date_time
    conditions = query_param.conditions
    file_name = query_param.file_name
    signals = query_param.signals

    voltage_conditions = []
    current_conditions = []
    frequency_conditions = []

    for condition in conditions:
        condition_type = condition.condition_type
        if condition_type == "voltage":
            voltage_conditions.append(condition.__str__())
        elif condition_type == "current":
            current_conditions.append(condition.__str__())
        else:
            frequency_conditions.append(condition.__str__())

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
