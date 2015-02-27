#!/usr/bin/python2.7
#
#  File:    DataEngine.py
#  Author:  Daniel E. Wilson
#
#  Collection of class to handle database accesses.
#
import os
import sys
import threading
import Queue

# Set up paths to handle DJango models.
# Assumes daemon lives in project directory.
projectHome = os.getcwd() + "/.."
sys.path.append(projectHome)
os.environ["DJANGO_SETTINGS_MODULE"] = "bpe_capstone.settings"
from stations.models import Station, Signal
from query.models import Query

class DataEngine(threading.Thread):
    "This class handles the database access for the daemon."

    def __init__(self):
        threading.Thread.__init__(self, None, self.run)
        self.daemon = True
        self.queue = Queue.Queue(-1)


    def run(self):
        "Function to handle the object to be added to the database."
        while True:
            model = self.queue.get(True)
            model.save()
            self.queue.task_done()

        def addSignals(self, PMUs, signals):
            "Add the PMUs and Signals to the queue."
            # Place the PMU objects in the queue.
            for p in PMUs:
                model = Station(PMU_ID = p['PMU_ID'],
                                PMU_Company = p['PMU_Company'],
                                PMU_Name_Raw = p['PMU_Name_Raw'],
                                PMU_Name_Short = p['PMU_Name_Short'],
                                PMU_Name_Long = p['PMU_Name_Long'],
                                PMU_Set = p['PMU_Set'],
                                PMU_Channel = p['PMU_Channel'],
                                PMU_Type = p['PMU_Type'],
                                PMU_Voltage = p['PMU_Voltage'])
                self.queue.put(model)

            # Place the Signal objects in the queue.
            for s in signals:
                model = Signal(Signal_ID = s['Signal_ID'],
                               Signal_PMU_ID = s['Signal_PMU_ID'],
                               Signal_Name_Raw = s['Signal_Name_Raw'],
                               Signal_Name_Short = s['Signal_Name_Short'],
                               Signal_Name_Group = s['Signal_Name_Group'],
                               Signal_Name_Long = s['Signal_Name_Long'],
                               Signal_Name_Type = s['Signal_Name_Type'],
                               Signal_Name_Asset = s['Signal_Name_Asset'],
                               Signal_Voltage = s['Signal_Voltage'],
                               Signal_Circuit = s['Signal_Circuit'],
                               Signal_Unit = s['Signal_Unit'],
                               Signal_Phase = s['Signal_Phase'])
                self.queue.put(model)

        def updateStatus(self, queryList, AnalysisList, StatusList):
            "Add all of the status reponses."
            # Loop through the query list.
            for qr in queryList:
                model = Query(query_name = str(qr['query_id']),
                              file_name = qr['file'])
                self.queue.put(model)

            # Loop through the analysis list.
            for ar in AnalysisList:
                model = {}
