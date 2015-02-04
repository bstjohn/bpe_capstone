from django.db import models

from django.contrib.auth.models import User

import json


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
    signal_measurement = models.CharField(max_length=24)
    signal_nominal_volts = models.IntegerField(max_length=3)
    signal_circuit_number = models.IntegerField(max_length=1)
    signal_measurement_identifier = models.CharField(max_length=24)
    signal_suffix = models.CharField(max_length=24)
    conditions = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=108, default="n/a")

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