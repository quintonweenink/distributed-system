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
		self.s = socket.socket()  # Create a socket object
		self.s.bind((self.host, self.port))  # Bind to the port

		self.s.listen(20)  # Now wait for client connection.
		while True:
			c, addr = self.s.accept()  # Establish connection with client.

			straddr = 'Got connection from' + str(addr)
			print straddr

			obj = json.loads(str(c.recv(1024)))
			print json.dumps(obj)



			self.captain.crew[0].res['message'] = "Connected to the Quartermaster"
			c.send(json.dumps(self.captain.crew[0].res))


			c.close()  # Close the connection
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


