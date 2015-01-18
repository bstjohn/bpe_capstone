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

class QueryHandler(SocketServer.StreamRequestHandler):
    "QueryHandler class for the query daemon."

    def handle(self):
        "Request handler function, each command is terminated by an empty line."

        # Data read loop.
        response=''
        while True:
            line = self.rfile.readline()
            if not line.strip():
                break
            else:
                response = response + line

        # Send the data back to the client.
        self.wfile.write(response)

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
