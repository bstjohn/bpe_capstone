# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Eric Olson, Brady St. John
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


from django.conf.urls import patterns, url

from query import views

urlpatterns = patterns('',
                       url(r'^$', views.query_index, name='query-index'),
                       url(r'^query-builder/', views.query_builder, name='query-builder'),
                       url(r'^query-result/', views.query_result, name='query-result'),
                       url(r'^status-result/', views.status_result, name='status-result')

)
