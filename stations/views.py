from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from stations.models import Station, Signal

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'stations/index.html'
    context_object_name = 'latest_station_list'

    def get_queryset(self):
        """Return station list."""
        return Station.objects.all()
