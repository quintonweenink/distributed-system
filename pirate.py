#!/usr/bin/python

import socket               # Import socket module
import json

import rummy

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.


def openConnection():
    s.connect((host, port))
    obj = json.loads(str(s.recv(1024)))
    print json.dumps(obj)

def closeConnection():
    s.close()


captain = rummy.Rummy("Manni", 5000)
print json.dumps(captain.wake())

#rum = rummy.Rummy("Manni", 5000)
openConnection()

data = {"data": "Thank you for connecting to the Pirate"}

s.send(json.dumps(data))

closeConnection()
