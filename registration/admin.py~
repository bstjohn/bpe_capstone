from django.contrib import admin
from registration.models import Person
from django.contrib.auth.models import User

# Unique email address
User._meta.get_field_by_name('email')[0]._unique = True
Person._meta.get_field_by_name('email')[0]._unique = True

# Register your models here.
class PersonRegistration(admin.ModelAdmin):
    readonly_fields = ('username',)

    fieldsets = [
        ('Enter Registration Code', {'fields': ['register_code']}),
        ('User Information', {'fields': ['username', 'email', 'first_name', 'last_name', ]}),
    ]
    list_display = ('register_code', 'username', 'email', 'first_name', 'last_name')

    # Set username read only, once created, it cannot be changed.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username']
        else:
            return []


admin.site.register(Person, PersonRegistration)
