# User admin site.
#
# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Shu Ping Chu
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from django.contrib import admin
from registration.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model # to import user model

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
