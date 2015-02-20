from django.contrib import admin
from registration.models import Person
from registration.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model # to import user model


# Register your models here.
class PersonRegistration(admin.ModelAdmin):
    readonly_fields = ('username',)

    fieldsets = [
        ('Enter Registration Code', {'fields': ['register_code']}),
        ('User Information', {'fields': ['username', 'email', 'first_name', 'last_name', ]}),
    ]
    list_display = ('register_code', 'username', 'email', 'first_name', 'last_name')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username']
        else:
            return []


admin.site.register(Person, PersonRegistration)


# User profile at admin site
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False   # not deleteable

# Add to the user admin
class UserProfileAdmin(UserAdmin):
    inlines =(UserProfileInline, )

# Grantee the user profile will be created successfully
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
