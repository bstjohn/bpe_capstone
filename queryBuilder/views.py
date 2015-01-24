from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from queryBuilder.forms import QueryForm, ConditionForm
from queryBuilder.models import Query


# Builds a query given user input
@login_required
def query_builder(request):
    condition_form_set = formset_factory(ConditionForm, extra=5, max_num=5)

    username = None
    if request.user.is_authenticated():
        username = request.user.username
        Query.user_name = username

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query_name = form.cleaned_data['query_name']
            return HttpResponseRedirect('/thanks/')
    else:
        form = QueryForm()

    context = {'username': username, 'form': form, 'formset': condition_form_set}
    return render(request, 'queryBuilder/query-builder.html', context)
