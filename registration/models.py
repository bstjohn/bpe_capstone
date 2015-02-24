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
