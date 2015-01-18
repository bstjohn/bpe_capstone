#!/usr/bin/python2.7
#
#  File:    QueryDaemon.py
#  Author:  Daniel E. Wilson
#
#  This is the Server daemon that holds performs the actual queries
#  once a user has initiated them from the Web interface.
#
#  This program should only be used with Python 2.7
#
import sys
import select
import SocketServer

class QueryHandler(SocketServer.BaseRequestHandler):
    "QueryHandler class for the query daemon."

    def handle(self):
        "Request handler function."
        size = 4096

        # Data read loop.
        response=''
        while True:
            data = self.request.recv(size)
            if len(data)<size:
                response = response + data
                break
            else:
                response = response + data

        # Send the data back to the client.
        self.request.sendall(response)

# Start the server.
if __name__=='__main__':

    # Set the hostname and port numbers.
    host = 'localhost'
    port = 4242

    # Create and run the server.
    server = SocketServer.TCPServer((host,port), QueryHandler)
    server.serve_forever()

    # End the program.
    sys.exit(0)
