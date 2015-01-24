from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from queryBuilder.forms import QueryForm, ConditionForm
from queryBuilder.models import Query

import time


# Builds a query given user input
@login_required
def query_builder(request):
    condition_form_set = formset_factory(ConditionForm, extra=5, max_num=5)

    username = None
    if request.user.is_authenticated():
        username = request.user.username
        Query.user_name = username
        Query.create_date_time = time.strftime("%c")

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query_name = form.cleaned_data['query_name']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']
            stations = form.cleaned_data['stations']
            condition_type = form.cleaned_data['condition_type']
            condition_operator = form.cleaned_data['condition_operator']
            condition_value = form.cleaned_data['condition_value']
            Query.query_name = query_name
            return HttpResponseRedirect('/thanks/')
    else:
        form = QueryForm()

    context = {'username': username, 'form': form, 'formset': condition_form_set}
    return render(request, 'queryBuilder/query-builder.html', context)
