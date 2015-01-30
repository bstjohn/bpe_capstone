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

class QueryEngine(threading.Thread):
    "Class that handles all of the queries to the BPA engine"

    def __init__(self):
        threading.Thread.__init__(self, None, self)
        self.queue = Queue.Queue(-1)

    def run(self):
        "Start the server task."
        while True:
            time.sleep(5)
