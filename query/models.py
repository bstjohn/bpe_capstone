from django.db import models

from django.contrib.auth.models import User

import json

# System Status model holding data for the system
class SystemStatus(models.Model):
    # not sure you need a owner
    sr_cpu = models.CommaSeparatedIntegerField(max_length=1024, null=True)
    sr_used = models.IntegerField(max_length=1024, null=True)
    sr_available = models.IntegerField(max_length=1024, null=True)
    

# Query model holding data from built queries
class Query(models.Model):
    # owner = models.OneToOneField(User)
    owner = models.ForeignKey(User, related_name="owners_query")
    user_name = models.CharField(max_length=24)
    create_date_time = models.DateTimeField('date created')
    query_name = models.CharField(max_length=100)
    start_date_time = models.DateTimeField('query start date time')
    end_date_time = models.DateTimeField('query end date time')
    stations = models.CharField(max_length=1024)
    conditions = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=108, default="n/a")
    status_field = models.CharField(max_length=1024, null=True)

    # QueryResponses
    qr_file = models.CharField(max_length=108, null=True)

    # AnalysisResponses
    ar_file = models.CharField(max_length=108, null=True)

    # Completed
    sr_completed = models.IntegerField(max_length=1024, null=True)


    # Set stations to a string from a json object
    def set_stations(self, stations):
        self.stations = json.dumps(stations)

    # Get stations as json object
    def get_stations(self):
        return json.loads(self.stations)

    # Set conditions to a string from a json object
    def set_conditions(self, conditions):
        self.conditions = json.dumps(conditions)

    # Get conditions as json object
    def get_conditions(self):
        return json.loads(self.conditions)

