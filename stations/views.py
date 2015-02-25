# Station and signal views.
#
# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Garrison Jensen
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
