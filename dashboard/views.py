# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Matei Mitaru
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, US$
#

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
