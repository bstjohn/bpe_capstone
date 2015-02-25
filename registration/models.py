# User profile models.
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

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User) # one to one relationship to user model
    # Extra attributes here!!
    cellphone = models.CharField(max_length=10, null=True) # user's cellphone, null is accetpable
    company = models.CharField(max_length=24, null=True)   # user's biography, null is accetpable

    # unicode representation
    def __unicode__(self):
        return "%s's profile" % unicode(self.user)

# User have profile property (if user have exist profile object, then get that one, or create a new profile object)
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
