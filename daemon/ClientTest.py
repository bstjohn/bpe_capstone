#!/usr/bin/python3.3
#
#  File:     ClientTest.py
#  Author:   Daniel E. Wilson
#
#  Test program to test commumincation with the client.
#
import sys
import QueryClient
import json

# Set the host and port number.
#host = '131.252.208.4'
#host = 'web.cecs.pdx.edu'
host = '131.252.42.50'
#host = 'localhost'
port = 1701

# Create the JSON object.
query= {'query': {'query_id': 3728,
                  'Signal_id': ['0x86d1-P-01'],
                  'start': '2014-10-31 14:00:00',
                  'end': '2014-10-31 14:30:00',
                  'analysisFile': '',
                  'pmu_channel': ['B'],
                  'pmu_company': ["GBPA"]}}

# Create the client instance.
client = QueryClient.BPAClient(host, port)

# Check to see if the query is correctly handled
result = client.startQuery(query)
print("Query result:")
print(json.dumps(result, indent=2))
print()

# Check to see if the signals request works.
result = client.getQueryStatus()
print("Query Status Result:")
print(json.dumps(result, indent=2))
print()

# Check the signals message
result = client.getSignals()
print("Signals Result:")
print(json.dumps(result, indent=2))
print()

# Successfule exit.
sys.exit(0)
