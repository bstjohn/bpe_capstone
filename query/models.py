# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Eric Olson, Brady St. John
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, US$
#


from django.db import models

from django.contrib.auth.models import User

import json


# System CPU
class SystemCpu(models.Model):
    # MANY cpus to ONE node
    node     = models.ForeignKey('SystemNode')
    cpu_id   = models.IntegerField(max_length=1024)
    cpu_load = models.FloatField(max_length=1024, default=0)

# System node, that contains information about disk space
class SystemNode(models.Model):
    # MANY nodes to ONE SystemStatus 
    system      = models.ForeignKey('SystemStatus')
    node_id     = models.IntegerField(max_length=100)    
    used        = models.IntegerField(max_length=1024, null=True)
    available   = models.IntegerField(max_length=1024, null=True)

    # calculate and return avg cpu
    def cpuAvg(self):
        total = 0
        num = 0
        for i in self.systemcpu_set.all():
          total += i.cpu_load
          num +=1
        if (num >0):
          return (int(total/num))
        else:
          return 0

    # calculate the color of the CPU box for the HTML page
    def boxColor(self):
        num = self.cpuAvg()
        # 0-25 = success / green color
        if num <25:
          return "success"
        # 26-50 = info  / blue color
        elif num >25 and num <=50:
          return "info"
        # 51-75 = warning / yellow color
        elif num >50 and num <=75:
          return "warning"
        # 75 < = danger/red color
        else:
          return "danger"

    # calculate the diskspace
    def diskSpace(self):
        return self.used/self.available
 

# System Status model holding data for the system, allows for multiple systems
class SystemStatus(models.Model):
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

