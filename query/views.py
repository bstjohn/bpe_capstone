# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Eric Olson, Brady St. John, Matei Mitaru
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, US$
#
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from query.forms import QueryForm, StationForm, StationFilterForm, SignalForm, SignalFilterForm
from query.models import Query, SystemStatus, SystemNode, SystemCpu
from stations.models import Station, Signal

import datetime
import time
import json
import socket


class QueryObject:
    """Object used to send a query defined by the user to be processed."""
    def __init__(self, model_id, start_date_time, end_date_time,
                 conditions, file_name, signals):
        self.model_id = model_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.conditions = conditions
        self.file_name = file_name
        self.signals = signals


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
    """Implementation of the /query/ endpoint."""
    return render(request, 'query/query.html')


@login_required
def query_result(request, pk):
    """Implementation of the /query-result/ endpoint."""
    query = Query.objects.filter(pk=pk)
    context = {'query':query}
    return render(request, 'query/query-result.html', context)


# Display the System Status
@login_required
def status_result(request):
    allqueries = Query.objects.all()
    sys_stat = SystemStatus.objects.all()    
    sys_cpu = SystemCpu.objects.all()
    sys_node = SystemNode.objects.all()
    # Calculate the information for the HTML page
    context = {'sys_stat': sys_stat, 'allqueries': allqueries,
               'sys_cpu': sys_cpu, 'sys_node': sys_node
 }
    return render(request, 'query/status-result.html', context)

# Global variable definitions
current_step = 0                                # The current step in the query builder process
stations = ''                                   # The stations specified by the user
query_model = Query()                           # The model persisted in the database
ss_model = SystemStatus()
query_object = QueryObject(None, None, None,    # The query that is sent to be processed
                           None, None, None)
ss_object = SystemStatusObject(None)
sn_object = SystemNodeObject(None, None, None)
scpu_object = SystemCpuObject(None, None)


# calculate and return a results page render
# - pass in a request and query model,
# - and return the rendered page 
@login_required
def return_result_page(request, query_model):
    context = {'query':query_model}
    return render(request, 'query/query-result.html', context)


def get_context(username, form, station_form, station_filter_form, signal_form,
                signal_filter_form, step):
    """Create a context to send to the front-end with the given parameters."""
    return {'username': username, 'form': form, 'station_form': station_form,
            'station_filter_form': station_filter_form, 'signal_form': signal_form,
            'signal_filter_form': signal_filter_form, 'current_step': step}


# Builds a query given user input
@login_required
def query_builder(request):
    """Implementation of the /query-builder/ endpoint."""

    # Global variables
    global query_model      # The model persisted in the database
    global query_object     # The query that is sent to be processed
    global current_step     # Current step in the builder
    global stations         # The stations selected by the user

    # Ensure the user has rights to the page and save their information:
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        query_model.user_name = username
        creation_date = time.strftime("%Y-%m-%d %H:%M:%S")
        query_model.create_date_time = creation_date

    # Instantiate blank form objects:
    if request.method == 'GET':
        detail_form = QueryForm()
        station_form = StationForm()
        station_filter_form = StationFilterForm(initial=StationFilterForm.get_initial_station_values())
        signal_form = SignalForm()
        signal_filter_form = SignalFilterForm(initial=SignalFilterForm.get_initial_signal_values())

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)

    # Request method is POST: Create and handle the forms with the given user input:
    detail_form = QueryForm(request.POST, request.FILES)
    signal_form = SignalForm(request.POST)
    signal_filter_form = SignalFilterForm(request.POST,
                                          initial=SignalFilterForm.get_initial_signal_values())
    station_form = StationForm(request.POST)
    station_filter_form = StationFilterForm(request.POST,
                                            initial=StationFilterForm.get_initial_station_values())
    # Save the first form data if the first form is valid and the user clicked 'next':
    if detail_form.is_valid() and 'save-details' in request.POST:
        # Re-make the signal_form object:
        signal_form = SignalForm()

        # Go to the next step in the process since the form submission was a success:
        current_step = 1

        # Retrieve user input from the front end and place it in the Query model:
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

        # Instantiate the query object that will be sent to be processed:
        query_object = QueryObject(None, start_date_time, end_date_time,
                                   None, file_name, None)

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
        current_step = 1

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
        current_step = 1

        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif station_form.is_valid() and 'station-submit' in request.POST:
        detail_form = QueryForm()
        current_step = 2

        # Retrieve the list of stations the user specified and update the signal form with those stations:
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

        current_step = 1
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif signal_filter_form.is_valid() and 'signal-filter-submit' in request.POST:
        detail_form = QueryForm()
        current_step = 2

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

        current_step = 2
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)
    elif signal_form.is_valid() and 'send' in request.POST:
        # A query was successfully defined. Save the model:
        query_model.save()

        # Further define the query object that will be sent and processed:
        query_object.model_id = query_model.id
        query_object.signals = request.POST.getlist('signals')

        # Convert the query object to JSON and send the results:
        json_query = convert_to_json(query_object)
        # send_to_server(json_query)

        # Finally, go to the result page
        return return_result_page(request, query_model)
    elif 'send' in request.POST:
        detail_form = QueryForm()
        current_step = 2
        context = get_context(username, detail_form, station_form, station_filter_form, signal_form,
                              signal_filter_form, current_step)
        return render(request, 'query/query-builder.html', context)


def get_stations(station_list):
    """Given a list of station strings, return the list of corresponding stations from the database.

    Keyword arguments:
    :param: station_list: the list of stations
    """
    station_objects = []
    for station in station_list:
        station_queryset = Station.objects.filter(PMU_Name_Short=station)
        station_objects = get_query_objects(station_queryset, station_objects)
    return station_objects


def get_query_objects(query_set, query_object_list):
    """Places the query objects contained in a query set into a list.

    Keyword arguments:
    :param: query_set: the QuerySet object to pull objects out of
    :param: query_object_list: the list to store query objects in
    """
    for query_field_object in query_set:
        query_object_list.append(query_field_object)
    return query_object_list


def convert_to_json(query_param):
    """Converts the given query object into a JSON object.

    Keyword arguments:
    :param: query_param: the query object to be converted to JSON
    """
    query_id = query_param.model_id
    start_date_time = query_param.start_date_time
    end_date_time = query_param.end_date_time
    file_name = query_param.file_name
    signals = query_param.signals

    # Get PMU Channel and Pmu Company attributes:
    pmu_channels = []
    pmu_companies = []
    for signal in signals:
        signal_objects = list(Signal.objects.filter(Signal_ID=int(signal))[:1])
        if signal_objects:
            signal_object = signal_objects[0]
            station = signal_object.Signal_PMU_ID
            pmu_channels.append(station.PMU_Channel)
            pmu_companies.append(station.PMU_Company)

    query = json.dumps({
        "query": {
            "query_id": query_id,
            "start": start_date_time.__str__(),
            "end": end_date_time.__str__(),
            "analysis_file": file_name,
            "signal_id": signals,
            "pmu_channel": pmu_channels,
            "pmu_company": pmu_companies
        }
    })

    return query


def send_to_server(json_query):
    """Send the query JSON object to the server.

    Keyword arguments:
    :param: json_query: the JSON object to send
    """
    # Set the server and host name to work with:
    host = 'localhost'
    port = 4242

    # Create the socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    f = s.makefile()
    try:
        # Now connect to the server:
        s.connect((host, port))
        f = s.makefile('rw', 4096)

        # Send the JSON object to the server:
        f.write(json_query)
        f.write('\n\n')
        f.flush()

    finally:
        f.close()
        s.close()
