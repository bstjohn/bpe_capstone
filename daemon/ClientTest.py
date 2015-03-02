#!/usr/bin/python3.3
#
#  File:     ClientTest.py
#  Author:   Daniel E. Wilson
#
#  Test program to test commumincation with the client.
#
#  Bonneville Power Adminstration Front-End
#  Copyright (C) 2015 Daniel E. Wilson.
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, US$
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
client = QueryClient.BPAClient(host, port)
result = client.getQueryStatus()
print("Query Status Result:")
print(json.dumps(result, indent=2))
print()

# Check the signals message
client = QueryClient.BPAClient(host, port)
result = client.getSignals()
print("Signals Result:")
print(json.dumps(result, indent=2))
print()

# Successfule exit.
sys.exit(0)
