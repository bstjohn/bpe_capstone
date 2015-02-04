#!/user/bin/python2.7
#
# File:    QueryClient.py
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
timeLimit = 5 * 60


class QueryEngine(threading.Thread):
    "Class that handles all of the queries to the BPA engine"

    def __init__(self):
        threading.Thread.__init__(self, None, self.run)
        self.daemon = True
        self.queue = Queue.Queue(25)

    def putQuery(self, query):
        "Add the query to the queue."
        self.queue.put(query, True, None)

    def run(self):
        "Start the server task."
        while True:
            # Get the next query from the queue.
            try:
                query = self.queue.get(True, timeLimit)

            # Query the BPA server if wait time exceeded.
            except Queue.Empty:
                print
                "Query the BPA server."

            else:
                # Process the query.
                try:
                    print
                    "Got query #{0}.".format(query['query']['id'])
                except KeyError:
                    print
                    "Invalid query in the queue."

                # Mark the current item as complete.
                self.queue.task_done()
