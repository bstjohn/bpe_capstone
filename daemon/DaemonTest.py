#!/usr/bin/python2.7
#
#  File:    DaemonTest.py
#  Author:  Daniel E. Wilson
#
#  This is a test program to see if the query daemon is correctly
#  responding to requests.
#
import sys
import json
import socket
import select

# Set the server and host name to work with.
host='localhost'
port=4242

# Create the socket.
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create the JSON object.
query= {'query': {'query_id': 3728,
                  'Signal_id': ['0x86d1-P-01'],
                  'start': '2014-10-31 14:00:00',
                  'end': '2014-10-31 14:30:00',
                  'analysisFile': '/this/dir/to/foo.r'}}

# Convert to a string.
queryString = json.dumps(query)

try:
    # Now connect to the server.
    s.connect((host,port))
    s.sendall(queryString + '\n\n')

    # Get read all of the response.
    s.setblocking(0)
    response=''
    while True:
        reading, writing, error = select.select([s],[],[],60)
        if reading:
            data = s.recv(1024)
            if not data:
                break
            else:
                response = response + data


    # Show the user what was send and recieved.
    print "Sent: {}".format(repr(query))
    print
    print "Received: {}".format(repr(response))

finally:
    s.close()

# End the program.
sys.exit(0)
