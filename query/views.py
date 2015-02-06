from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import formset_factory

from query.forms import QueryForm, ConditionForm
from query.models import Query

import datetime
import time
import json
import os


@login_required
def query_index(request):
    return render(request, 'query/query.html')


# Builds a query given user input
@login_required
def query_builder(request):
    condition_form_set = formset_factory(ConditionForm, extra=1)
    username = None
    creation_date = None
    query_model = Query()
    if request.user.is_authenticated():
        username = request.user.username
        query_model.user_name = username
        creation_date = time.strftime("%Y-%m-%d %H:%M:%S")
        query_model.create_date_time = creation_date

    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        condition_form = condition_form_set(request.POST)
        if form.is_valid() and condition_form.is_valid():
            query_model.owner = request.user
            query_model.query_name = form.cleaned_data['query_name']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            start_date_time = datetime.datetime.combine(start_date, start_time)
            query_model.start_date_time = start_date_time
            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']
            end_date_time = datetime.datetime.combine(end_date, end_time)
            query_model.end_date_time = end_date_time
            stations = form.cleaned_data['stations']
            query_model.set_stations(stations)
            condition_type = form.cleaned_data['condition_type']
            condition_operator = form.cleaned_data['condition_operator']
            condition_value = form.cleaned_data['condition_value']
            primary_condition = Condition(condition_type, condition_operator, condition_value)
            conditions = [primary_condition]

            for condition_field in condition_form:
                condition = Condition(condition_field.cleaned_data['condition_type'],
                                      condition_field.cleaned_data['condition_operator'],
                                      condition_field.cleaned_data['condition_value'])
                if condition.condition_value is not None:
                    conditions.append(condition)
            condition_strings = []
            for condition in conditions:
                condition_strings.append(condition.__str__())
            query_model.set_conditions(condition_strings)

            file = request.FILES["file"]
            file_name = file.name
            query_model.file_name = file_name
            query_model.save()

            print(convert_to_json(query_model.id, creation_date, start_date_time, end_date_time,
                                  stations, conditions, file_name))

            return HttpResponseRedirect('/query/query-result/')
    else:
        form = QueryForm()

    context = {'username': username, 'form': form, 'formset': condition_form_set}
    return render(request, 'query/query-builder.html', context)


def get_file_type(file_path):
    return file_path.split(".")[-1]


def stringify_file(file_path):
    data = ""
    with open(file_path.name, "rb"):
        for chunk in file_path.chunks():
            data += chunk.decode(encoding='UTF-8').replace('\r\n', '')

    return data


def save_file(file_path):
    destination = open(file_path.name, "wb")
    for chunk in file_path.chunks():
        destination.write(chunk)
    destination.close()


def delete_file(file_path):
    os.remove(file_path.name)


def convert_to_json(query_id, creation_date, start_date_time, end_date_time,
                    stations, conditions, file_name):
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
            "created": creation_date.__str__(),
            "start": start_date_time.__str__(),
            "end": end_date_time.__str__(),
            "stations": stations,
            "analysis_file": file_name,
            "signal_id": ""
        }
    })

    return query


class Condition:
    def __init__(self, condition_type, condition_operator, condition_value):
        self.condition_type = condition_type
        self.condition_operator = condition_operator
        self.condition_value = condition_value

    def __str__(self):
        return self.condition_type + " " + self.condition_operator + " " + str(self.condition_value)