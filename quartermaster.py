#!/usr/bin/python

import socket
import json

s = {}
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.

def listenDispatch ():
    s = socket.socket()  # Create a socket object
    s.bind((host, port))  # Bind to the port

    s.listen(5)  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        straddr = 'Got connection from', addr
        print straddr
        obj = {"data": "Thank you for connecting to the Quartermaster"}
        c.send(json.dumps(obj))
        obj = json.loads(str(c.recv(1024)))
        print json.dumps(obj)
        c.close()  # Close the connection
    return

listenDispatch()
