from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def query_builder(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    context = {'username': username}
    return render(request, 'queryBuilder/query-builder.html', context)