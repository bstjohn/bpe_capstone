from django.shortcuts import render


from django.contrib.auth.decorators import login_required


@login_required
def get_results(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    context = {'username': username}
    #return render(request, 'results/results.html', context)
    return render(request, '/results/get-results/', context)
