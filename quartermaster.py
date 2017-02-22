#!/usr/bin/python

import socket
import json

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   straddr = 'Got connection from', addr
   print straddr
   obj = {"data":"Thank you for connecting"}
   c.send(json.dumps(obj))
   c.close()                # Close the connection
