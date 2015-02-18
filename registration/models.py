import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Person model
class Person(models.Model):
    register_code = models.CharField(max_length=24)
    username = models.CharField(max_length=24)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    create_date = models.DateTimeField('create_date', auto_now=True)

    # make formate looks nicer
    # ex: [<Person: person 1 >, <Person: person 2 >, <Person: person 3 >]
    def __unicode__(self):
        return self.first_name

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.register_code, self.username,
                                      self.email, self.first_name,
                                      self.last_name, self.create_date)


# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User) # one to one relationship to user model
    # Extra attributes here!!
    cellphone = models.CharField(max_length=10, null=True) # user's cellphone, null is accetpable
    bio = models.TextField(null=True)                      # user's biography, null is accetpable

    # unicode representation
    def __unicode__(self):
        return "%s's profile" % unicode(self.user)

# User have profile property (if user have exist profile object, then get that one, or create a new profile object)
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])








