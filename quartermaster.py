#!/usr/bin/python

import socket
import json
import sys

execfile("rummy.py")

#Spool up different pirates in command line

class Quartermaster:

    state = 0

    def __init__(self, crewSize):
        self.s = {}
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12359  # Reserve a port for your service.
        self.crewSize = crewSize
        self.clueList = []

        print "========== QUARTERMASTER ======="

        print "ARRGG.. STARTING "
        print "PORT: ", self.port
        print "Crew Size: ", self.crewSize

        print "================================"
        print ""

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to the port

        self.s.listen(20)  # Now wait for client connection.

        self.captain = Rummy(crewSize)

    def toString(self):
        self.captain.printCrew()

    def addToClueList(self, id, data):
        clue = {"id": id, "data": [data]}
        self.clueList.append(clue)

    def isDone(self):
        for member in self.captain.crew:
            if len(member.clues) > 0:
                return False
        return True


    def listenDispatch(self):

        while not self.isDone():

            if not self.isDone():
                c, addr = self.s.accept()  # Establish connection with client.
                obj = json.loads(str(c.recv(1024)))

                #print json.dumps(obj)
                if obj["id"] == -1:
                    for member in self.captain.crew:
                        if member.connected == False:
                            member.connected = True
                            member.getClue()

                            c.send(json.dumps(member.res))
                            break
                else:
                    for member in self.captain.crew:
                        if member.res['id'] == obj["id"]:
                            member.getClue()
                            if obj['data'] != "wait":
                                self.addToClueList(member.res['id'], obj['data'])
                            member.cluesSolved += 1

                            c.send(json.dumps(member.res))
                            break

                c.close()  # Close the connection

            sys.stdout.write("X")
            sys.stdout.flush()


            if len(self.clueList) > 49 or self.isDone():
                rummyObj = self.captain.verify(self.clueList)
                self.clueList = []

                if 'finished' in rummyObj:
                    print "YOU COMPLETED THE PROBLEM"
                elif rummyObj['status'] == "error":
                    data = rummyObj['data']
                    for clueError in data:
                        for member in self.captain.crew:
                            if member.res['id'] == clueError["id"]:
                                for error in clueError['data']:
                                    member.clues.append(error)
                                    member.cluesSolved -= 1
                                    member.failed += 1
                            elif len(member.clues) == 0:
                                member.res["finished"] = True

                print ""
                print "========== MY PIRATES =========="
                for pirate in self.captain.crew:
                    pirate.toString()
                print "================================"
                print ""
                print 'Next clue set: '



        print "YOU HAVE COMPLETED THE PROBLEM"


quartermaster = Quartermaster(5)
quartermaster.listenDispatch()


