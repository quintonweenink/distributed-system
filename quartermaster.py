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
        self.port = 12482  # Reserve a port for your service.
        self.crewSize = crewSize

        print "========== QUARTERMASTER ======="

        print "ARRGG.. STARTING "
        print "PORT: ", self.port
        print "Crew Size: ", self.crewSize

        print "================================"

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to the port

        self.s.listen(20)  # Now wait for client connection.

        self.captain = Rummy(crewSize)

    def toString(self):
        self.captain.printCrew()


    def listenDispatch(self):
        clueList = []
        isDone = False
        while not isDone:
            c, addr = self.s.accept()  # Establish connection with client.

            obj = json.loads(str(c.recv(1024)))

            #print json.dumps(obj)
            if obj["id"] == -1:
                for member in self.captain.crew:
                    if member.connected == False:
                        member.res['message'] = "Connected to the Quartermaster. Giving you an id and clue"
                        if len(member.clues) >= 1:
                            member.res['data'] = member.clues.pop()
                        else:
                            member.res['data'] = ""
                        member.connected = True
                        c.send(json.dumps(member.res))
                        break
            else:
                for member in self.captain.crew:
                    if member.res['id'] == obj["id"]:
                        member.res['message'] = "You are finished, Lets get you another clue"
                        if len(member.clues) >= 1:
                            member.res['data'] = member.clues.pop()
                        else:
                            member.res['data'] = ""
                        clue = {"id": member.res["id"], "data": [obj['data']]}
                        clueList.append(clue)
                        member.cluesSolved += 1
                        c.send(json.dumps(member.res))
                        break

            print 'X',

            if len(clueList) > 9:
                rummyObj = self.captain.verify(clueList)
                #print json.dumps(rummyObj)
                clueList = []

                if 'finished' in rummyObj:
                    print "YOU COMPLETED THE PROBLEM"
                elif rummyObj['status'] == "error":
                    data = rummyObj['data']
                    for clueError in data:
                        for member in self.captain.crew:
                            if member.res['id'] == clueError["id"]:
                                for error in clueError['data']:
                                    member.clues.append(error)
                                    #print "Clue Error: " + json.dumps(error)
                                    member.cluesSolved -= 1


                print "========== MY PIRATES =========="
                for pirate in self.captain.crew:
                    print "{"
                    pirate.toString()
                    print "}"
                print "================================"
                print 'Next clue set: ',

            isDone = True
            for member in self.captain.crew:
                if len(member.clues) != 0:
                    isDone = False



            c.close()  # Close the connection

        if len(clueList) > 0:
            rummyObj = self.captain.verify(clueList)
            # print json.dumps(rummyObj)

            if 'finished' in rummyObj:
                print "GOT FINISHED RESPONSE"
            elif rummyObj['status'] == "error":
                data = rummyObj['data']
                for clueError in data:
                    for member in self.captain.crew:
                        if member.res['id'] == clueError["id"]:
                            for error in clueError['data']:
                                member.clues.append(error)
                                # print "Clue Error: " + json.dumps(error)
                                member.cluesSolved -= 1


        print "YOU HAVE COMPLETED THE PROBLEM"


quartermaster = Quartermaster(5)
quartermaster.listenDispatch()


