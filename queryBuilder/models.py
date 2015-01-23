from django.db import models

import json


# Query model holding data from built queries
class Query(models.Model):
    user_name = models.CharField(max_length=24)
    create_date = models.DateTimeField('date created')
    start_date_time = models.DateTimeField('query start date time')
    end_date_time = models.DateTimeField('query end date time')
    stations = models.CharField(max_length=1000)

    # Set stations to a string from a json object
    def set_stations(self, stations):
        self.stations = json.dumps(stations)

    # Get stations as json object
    def get_stations(self):
        return json.loads(self.stations)