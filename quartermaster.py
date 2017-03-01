#!/usr/bin/python

import socket
import json

execfile("rummy.py")

#Spool up different pirates in command line

class Quartermaster:

    state = 0

    def __init__(self, crewSize):
        self.s = {}
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12345  # Reserve a port for your service.

        self.captain = Rummy(crewSize)

    def toString(self):
        self.captain.printCrew()


    def listenDispatch(self):
        s = socket.socket()  # Create a socket object
        s.bind((self.host, self.port))  # Bind to the port

        s.listen(20)  # Now wait for client connection.
        while True:
            print json.dumps(self.captain.wake())

            c, addr = s.accept()  # Establish connection with client.

            straddr = 'Got connection from' + str(addr)
            print straddr
            obj = {"data": "Thank you for connecting to the Quartermaster"}
            c.send(json.dumps(obj))
            obj = json.loads(str(c.recv(1024)))

            print json.dumps(obj)
            c.close()  # Close the connection

            for pirate in self.captain.crew:
                print "{"
                pirate.toString()
                print "}"
        return

quartermaster = Quartermaster(5)
quartermaster.listenDispatch()

# PSUDO CODE:
#
#     BEGIN:
#         ASK RUMMY FOR PIRATE ID'S:
#         INIT THE OBJECTS WITH ID'S AND MAYBE THE CONNECTIONS
#         START UP AGENTS IN CONSOLE:
#         SEND THEM THEIR ID'S
#
#         LET THEM SIT AND TRY CONNECT WHILE BUSY SETTING UP THE OTHERS
#
#         LOOP OVER CONNECTIONS
#             GIVE WHOEVER ASKS A TASK TO COMPLETE


