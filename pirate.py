#!/usr/bin/python

import socket               # Import socket module
import json
import subprocess

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
obj = json.loads(str(s.recv(1024)))
print json.dumps(obj)
args = ["python", "rummy.pyc", "-w"]
output = subprocess.check_output(args).strip()
obj = json.loads(str(output))
print json.dumps(obj)
s.close                     # Close the socket when done
