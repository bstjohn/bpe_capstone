#!/user/bin/python2.7
#
#  File:    QueryClient.py
#  Author:  Daniel E. Wilson
#
#  File of classes to handle the queries in the backend of
#  the BPA database.
#
import Queue
import threading
import time

# Set the host name and port number of the database engine.
host = 'localhost'
port = 1701

# Set the default time limit
timeLimit = 5*60

class QueryEngine(threading.Thread):
    "Class that handles all of the queries to the BPA engine"

    def __init__(self):
        threading.Thread.__init__(self, None, self.run)
        self.daemon = True
        self.queue = Queue.Queue(25)
        self.client = BPAClient(host, port)
        self.lastHour = None

    def putQuery(self, query):
        "Add the query to the queue."
        self.queue.put(query, True, None)

    def run(self):
        "Start the server task."
        while True:
            # Get list of signals after midnight.
            if self.afterMidnight():
                signals = self.client.getSignals()

            # Get the next query from the queue.
            try:
                query = self.queue.get(True, timeLimit)

            # Query the BPA server if wait time exceeded.
            except Queue.Empty:
                currentStatus = self.client.getQueryStatus()

            else:
                # Submit the query to the BPA server.
                status, msg, result = self.client.startQuery(query)
                if status<>0:
                    print "Query Error #{0}: {1}".format(status, msg)

                # Mark the current item as complete.
                self.queue.task_done()

    def afterMidnight(self):
        "Check to see if midnight has passed."
        if self.lastHour == None:
            now = time.localtime()
            self.lastHour = now.tm_hour
            status = False
        else:
            now = time.localtime()
            hour = now.tm_hour
            status = hour < self.lastHour
            self.lastHour = hour
        return status


class BPAClient:
    "Class that will handle communication with the BPA database."

    def __init__(self, host, port):
        pass

    def getQueryStatus(self):
        "Get the status of all runncing queries from the BPA server."
        return None

    def startQuery(self, query):
        "Start a new query on the BPA server."
        return (0, "Success", {})

    def getSignals(self):
        "Get the signals from the BPA Server."
        return None
