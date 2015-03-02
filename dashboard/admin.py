# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Garrison Jenson, Matei Mitaru
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

from django.contrib import admin

from dashboard.models import Dashboard
from query.models import Query

class DashboardAdmin(admin.ModelAdmin):
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        has_class_permission = \
            super(DashboardAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser \
                and request.user.id != obj.author.id:
            return False
        return True


class QueryAdmin(admin.ModelAdmin):
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        has_class_permission = \
            super(QueryAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser \
                and request.user.id != obj.author.id:
            return False
        return True



admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Query, QueryAdmin)
