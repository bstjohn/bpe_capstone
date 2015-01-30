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
import QueryClient

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

    # Create the query engine object and start it.
    queryEngine = QueryClient.QueryEngine()
    queryEngine.start()

    # Create and run the server.
    server = SocketServer.TCPServer((host,port), QueryHandler)
    server.serve_forever()

    # End the program.
    sys.exit(0)
