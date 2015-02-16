from django.contrib import admin
from query.models import SystemCpu, SystemNode, SystemStatus, Query

# Register your models here.
admin.site.register(SystemCpu)
admin.site.register(SystemNode)
admin.site.register(SystemStatus)
#admin.site.register(Query)
