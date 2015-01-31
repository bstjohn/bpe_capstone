from django.contrib import admin

from dashboard.models import Dashboard
from queryBuilder.models import Query


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