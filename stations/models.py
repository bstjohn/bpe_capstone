# Signal and station models.
#
# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Garrison Jensen
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

from django.db import models

# Create your models here.

class Station(models.Model):
    PMU_ID         = models.IntegerField(primary_key=True)  # "[0x84e1]"
    PMU_Company    = models.CharField(max_length=200) # "GBPA"
    PMU_Name_Raw   = models.CharField(max_length=200) # "ALBN 500 B1 SA "
    PMU_Name_Short = models.CharField(max_length=200) # "ALBN"
    PMU_Name_Long  = models.CharField(max_length=200) # "Albion"
    PMU_Set        = models.IntegerField(default=-1)  # 1
    PMU_Channel    = models.CharField(max_length=1)   # "B",
    PMU_Type       = models.CharField(max_length=5)   # "SA",
    PMU_Voltage    = models.IntegerField(default=-1)  # 500

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (hex(self.PMU_ID), self.PMU_Company, self.PMU_Name_Raw,
                                               self.PMU_Name_Short, self.PMU_Name_Long, self.PMU_Set,
                                               self.PMU_Channel, self.PMU_Type, self.PMU_Voltage)


class Signal(models.Model):
    Signal_ID         = models.CharField(max_length=200)
    Signal_PMU_ID     = models.ForeignKey('Station')
    Signal_Index      = models.IntegerField(default=-1)
    Signal_Name_Raw   = models.CharField(max_length=200)
    Signal_Name_Short = models.CharField(max_length=200)
    Signal_Name_Group = models.CharField(max_length=200)
    Signal_Name_Long  = models.CharField(max_length=200)
    Signal_Type       = models.CharField(max_length=200)
    Signal_Asset      = models.CharField(max_length=200)
    Signal_Voltage    = models.IntegerField(default=-1)
    Signal_Circuit    = models.IntegerField(default=-1)
    Signal_Unit       = models.CharField(max_length=200)
    Signal_Phase      = models.CharField(max_length=200)

    def __str__(self):
        pmu_id = self.Signal_PMU_ID.PMU_ID
        return '%s, PMU: %s, %s, %s, %s, %s, %s, %s, %s' % (self.Signal_ID, pmu_id, self.Signal_Index,
                                                           self.Signal_Type, self.Signal_Asset, self.Signal_Voltage,
                                                           self.Signal_Circuit, self.Signal_Unit, self.Signal_Phase)
