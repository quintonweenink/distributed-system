#!/usr/bin/python

import socket               # Import socket module
import json
import time

s = socket.socket()  # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

id = -1;


def openConnection():
    s.connect((host, port))
    obj = json.loads(str(s.recv(1024)))
    print json.dumps(obj)

def closeConnection():
    s.close()



openConnection()

data = {"data": "Thank you for connecting to the Pirate",
        "id": str(id)}
s.send(json.dumps(data))

closeConnection()


time.sleep(5) # delays for 10 seconds

s = socket.socket()  # Create a socket object


openConnection()

id = 0

data = {"data": "Thank you for your time",
        "id": str(id)}
s.send(json.dumps(data))

closeConnection()
