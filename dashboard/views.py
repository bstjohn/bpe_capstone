from django.shortcuts import render


def dashboard(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    context = {'username': username}
    return render(request, 'dashboard/dashboard.html', context)