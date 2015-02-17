import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
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
