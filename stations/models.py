from django.db import models

# Create your models here.

class Station(models.Model):
    PMU_ID         = models.IntegerField(default=-1)  # "[0x84e1]"
    PMU_Company    = models.CharField(max_length=200) # "GBPA"
    PMU_Name_Raw   = models.CharField(max_length=200) # "ALBN 500 B1 SA "
    PMU_Name_Short = models.CharField(max_length=200) # "ALBN"
    PMU_Name_Long  = models.CharField(max_length=200) # "Albion"
    PMU_Set        = models.IntegerField(default=-1)  # 1
    PMU_Channel    = models.CharField(max_length=1)   # "B",
    PMU_Type       = models.CharField(max_length=5)   # "SA",
    PMU_Voltage    = models.IntegerField(default=-1)  # 500

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.PMU_ID, self.PMU_Company, self.PMU_Name_Raw, self.PMU_Name_Short, self.PMU_Name_Long, self.PMU_Set, self.PMU_Channel, self.PMU_Type, self.PMU_Voltage)


class Signal(models.Model):
    Signal_ID         = models.IntegerField(default=-1)
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
