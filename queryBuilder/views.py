from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from queryBuilder.forms import QueryForm
from queryBuilder.models import Query


# Builds a query given user input
@login_required
def query_builder(request):
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
        form.as_table()

    context = {'username': username, 'form': form}
    return render(request, 'queryBuilder/query-builder.html', context)
