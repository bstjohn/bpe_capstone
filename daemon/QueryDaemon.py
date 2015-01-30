#!/usr/bin/python2.7
#
#  File:    QueryDaemon.py
#  Author:  Daniel E. Wilson
#
#  This is the Server daemon that holds performs the actual queries
#  once a user has initiated them from the Web interface.
#
#  This program should only be used with Python 2.7 interprester.
#
import sys
import json
import select
import SocketServer
import threading


class Queue:
    "Object to hold a queue of items to be processed."

    def __init__(self):
        self.queue = []
        self.condition = threading.Condition()

    def push(self, request):
        "Add an item to the request queue."
        with self.condition:
            self.queue.append(request)

    def pushList(self, lst):
        "Push a list of items on to the queue."
        with self.condition:
            for item in lst:
                self.queue.append(item)

    def deque(self):
        "Remove an item from the queue."
        with self.condition:
            while not self.queue:
                self.condition.wait()
            result = self.queue[0]
            del self.queue[0]
        return result

    def deque_nb(self):
        "Get an item from the queue with no waiting."
        with self.condition:
            if self.queue:
                result = self.queue[0]
            else:
                result = None
        return result

    def drop(self):
        "Drop the first item from the queue."
        with self.condition:
            if len(self.queue)>0:
                del self.queue[0]

    def __len__(self):
        "Get the number of items on the queue."
        with self.condition:
            result = len(self.queue)
        return result


class QueryHandler(SocketServer.StreamRequestHandler):
    "QueryHandler class for the query daemon."

    def readQuery(self):
        "Read the query from the socket."
        response=''
        while True:
            line = self.rfile.readline()
            if not line.strip():
                break
            else:
                response = response + line
        return response

    def handle(self):
        "Request handler function, each command is terminated by an empty line."
        # Get the query text.
        request = self.readQuery()

        # Get the JSON object from the text.
        query = json.loads(request)

        # Create response object.
        if query.has_key('query'):
            a = {'code': 0, 'msg': "SUCCESS"}
        else:
            a = {'code': 1, 'msg': "Not a valid query object."}
        response = {'status': a}

        # Send the data back to the client.
        json.dump(response, self.wfile)
        self.wfile.write('\n\n')

# Start the server.
if __name__=='__main__':

    # Set the hostname and port numbers.
    host = 'localhost'
    port = 4242

    # Initialize the query queue.
    queue = QueryQueue()

    # Create and run the server.
    server = SocketServer.TCPServer((host,port), QueryHandler)
    server.serve_forever()

    # End the program.
    sys.exit(0)
