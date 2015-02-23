from django.contrib import admin
from registration.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model # to import user model

# Set UserAdminForm username read only at admin site, once created, it cannot be changed.
admin.site.unregister(User)

class UserAdminForm(UserAdmin):
    # here we can add more fields to make read only!
    readonly_fields = ('username',)

admin.site.register(User, UserAdminForm)


# Unique email address for user and person class
User._meta.get_field_by_name('email')[0]._unique = True

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

