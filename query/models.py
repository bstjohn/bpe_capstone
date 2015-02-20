from django.db import models

from django.contrib.auth.models import User

import json


# System CPU, which is one of many CPU's that live inside a node.
class SystemCpu(models.Model):
    # MANY cpus to ONE node
    node     = models.ForeignKey('SystemNode')
    cpu_id   = models.IntegerField(max_length=1024)
    cpu_load = models.FloatField(max_length=1024, default=0)

# System node, that contains information about disk space as well as 
# CPU's
class SystemNode(models.Model):
    # MANY nodes to ONE SystemStatus 
    system      = models.ForeignKey('SystemStatus')
    node_id     = models.IntegerField(max_length=100)    
    used        = models.IntegerField(max_length=1024, null=True)
    available   = models.IntegerField(max_length=1024, null=True)

    def diskSpace(self):
        return self.used/self.available
 

# System Status model holding data for the system
class SystemStatus(models.Model):
    # not sure you need a owner
    # sr_cpu = models.CommaSeparatedIntegerField(max_length=1024, null=True)
    system_id = models.IntegerField(max_length=10)

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

