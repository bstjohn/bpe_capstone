from django.contrib import admin
from registration.models import Person
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Set UserAdminForm username read only at admin site, once created, it cannot be changed.
admin.site.unregister(User)

class UserAdminForm(UserAdmin):
    # here we can add more fields to make read only!
    readonly_fields = ('username',)

admin.site.register(User, UserAdminForm)


# Unique email address for user and person class
User._meta.get_field_by_name('email')[0]._unique = True
Person._meta.get_field_by_name('email')[0]._unique = True

# Register your person models here.
class PersonRegistration(admin.ModelAdmin):
    readonly_fields = ('username',) # read only for Person.username

    fieldsets = [
        ('Enter Registration Code', {'fields': ['register_code']}),
        ('User Information', {'fields': ['username', 'email', 'first_name', 'last_name', ]}),
    ]
    # display list base of fields order
    list_display = ('register_code', 'username', 'email', 'first_name', 'last_name')

    # Set Person.username read only, once created, it cannot be changed.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username']
        else:
            return []
# Register Person at admin site
admin.site.register(Person, PersonRegistration)
