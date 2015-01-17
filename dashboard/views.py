from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
