from django.shortcuts import render
from query.models import Query
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    allqueries = Query.objects.all()
    myqueries = Query.objects.filter(user_name = username)
    context = {'username': username, 'allqueries':allqueries, 'myqueries':myqueries}
    return render(request, 'dashboard/dashboard.html', context)
