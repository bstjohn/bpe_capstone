from django.contrib import admin
from registration.models import Person

# Register your models here.
class PersonRegistrationCode(admin.ModelAdmin):
	fieldsets = [
		('Enter Registration Code', {'fields': ['registration_code']}),
                ('User Information', {'fields': ['first_name', 'last_name', 
                                                 'user_name', 'user_password',
                                                 'email_addr', 'create_date',]}),
                    ]

admin.site.register(Person, PersonRegistrationCode)
