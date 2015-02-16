#!/usr/bin/python2.7
#
# File:    DaemonTest.py
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
host = 'localhost'
port = 4242

# Create the socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create the JSON object.
query= {'query': {'query_id': 3728,
                  'Signal_id': ['0x86d1-P-01'],
                  'start': '2014-10-31 14:00:00',
                  'end': '2014-10-31 14:30:00',
                  'analysisFile': '/this/dir/to/foo.r'}}

try:
    # Now connect to the server.
    s.connect((host,port))
    f = s.makefile('rw', 4096)

    # Send the JSON object to the server.
    json.dump(query, f)
    f.write('\n\n')
    f.flush()

    # Get read all of the response.
    response=''
    while True:
        line = f.readline()
        if not line.strip():
            break
        else:
            response = response + line

    # Show the user what was send and recieved.
    print "Sent: {}".format(repr(query))
    print
    print "Received: '{}'".format(response.strip())

finally:
    f.close()
    s.close()

# End the program.
sys.exit(0)
