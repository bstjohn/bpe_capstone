from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from queryBuilder.forms import QueryForm, ConditionForm
from queryBuilder.models import Query

import datetime
import time
import json


def handle_uploaded_file(file_path):
    destination = open(file_path.name, "wb")
    for chunk in file_path.chunks():
        destination.write(chunk)
    destination.close()

# Builds a query given user input
@login_required
def query_builder(request):
    condition_form_set = formset_factory(ConditionForm, extra=3, max_num=3)
    username = None
    creation_date = None
    query_model = Query()
    if request.user.is_authenticated():
        username = request.user.username
        query_model.user_name = username
        creation_date = time.strftime("%Y-%m-%d %H:%M")
        query_model.create_date_time = creation_date

    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        condition_form = condition_form_set(request.POST)
        if form.is_valid() and condition_form.is_valid():
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
            conditions = []
            condition_type = form.cleaned_data['condition_type']
            condition_operator = form.cleaned_data['condition_operator']
            condition_value = form.cleaned_data['condition_value']
            primary_condition = Condition(condition_type, condition_operator, condition_value)
            conditions.append(primary_condition)

            for condition_field in condition_form:
                condition = Condition(condition_field.cleaned_data['condition_type'],
                                      condition_field.cleaned_data['condition_operator'],
                                      condition_field.cleaned_data['condition_value'])
                conditions.append(condition)

            query_model.save()

            print(convert_to_json(username, query_model.id, creation_date, start_date_time, end_date_time,
                            stations, conditions, "blah", "r"))

            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect('/query-result/')
    else:
        form = QueryForm()

    context = {'username': username, 'form': form, 'formset': condition_form_set}
    return render(request, 'queryBuilder/query-builder.html', context)


def convert_to_json(user_name, query_id, creation_date, start_date_time, end_date_time,
                    stations, conditions, file_name, file_type):

    query = json.dumps({
        "query": {
            "query_id": "",
            "created": creation_date.__str__(),
            "start": start_date_time.__str__(),
            "end": end_date_time.__str__(),
            "stations": stations,
            "attributes": {
                "voltage": {},
                "current": {},
                "freq": {},
                "nomvolts": ""
            },
            "user": {
                "name": user_name,
            },
            "analysis": {
                "file": file_name,
                "type": file_type,
            },
        }
    })

    return query


class Condition:
    def __init__(self, condition_type, condition_operator, condition_value):
        self.condition_type = condition_type
        self.condition_operator = condition_operator
        self.condition_value = condition_value
