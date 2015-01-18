#!/usr/bin/python2.7
#
#  File:    DaemonTest.py
#  Author:  Daniel E. Wilson
#
#  This is a test program to see if the query daemon is correctly
#  responding to requests.
#
import sys
import socket
import select

# Set the server and host name to work with.
host='localhost'
port=4242

# Create the socket.
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the test text.
txt="This is a test.\nThis is another test.\n"

try:
    # Now connect to the server.
    s.connect((host,port))
    s.sendall(txt)

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
    print "Sent: {}".format(txt)
    print "Received: {}".format(response)

finally:
    s.close()

# End the program.
sys.exit(0)
