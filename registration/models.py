import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    registration_code = models.CharField(max_length=24)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    user_name = models.CharField(max_length=24)
    user_password = models.CharField(max_length=24)
    email_addr = models.CharField(max_length=100)
    create_date = models.DateTimeField('date created')
    
    def __str__(self):
	return '%s %s %s %s %s %s %s' % (self.registration_code,
					 self.first_name, self.last_name,  
                                         self.user_name, self.user_password,
                                         self.email_addr, self.create_date)
