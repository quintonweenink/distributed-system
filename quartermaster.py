#!/usr/bin/python

import socket
import json
import sys
import time

execfile("irummy.py")

# Master
class Quartermaster:

    def __init__(self):
        self.s = {}
        self.host = socket.gethostname()  # Get local machine name
        self.port = int(sys.argv[1])   # Reserve a port for your service.
        self.crewSize = int(sys.argv[2])
        self.clueList = []
        self.verifyListSize = 500
        self.mapListSize = 20.0
        self.clueListSize = 1000.0

        self.numClue = 0
        self.numMap = 0
        self.numMapClue = 0

        print "========== QUARTERMASTER ======="

        print "ARRGG.. STARTING "
        print "PORT: ", self.port
        print "Crew Size: ", self.crewSize

        print "================================"
        print ""

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to

        #  the port
        self.s.listen(20)  # Now wait for client connection.

        self.captain = iRummy(self.crewSize, self.port)
        self.startPirates()

    def listenDispatch(self):
        print self.printPirates() + self.printProblemState()

        while True:
            self.captain.getPirateClues()
            self.numMapClue = 0


            for member in self.captain.crew:
                member.paused = False
                member.cluesSolved = 0
                member.failed = 0

            while not self.isAllDead() or len(self.clueList) > 0:

                if not self.isAllDead():
                    c, addr = self.s.accept()
                    obj = json.loads(str(c.recv(1024)))
                    if obj["id"] == -1:
                        for member in self.captain.crew:
                            if member.connected == False:
                                member.connected = True
                                member.getClue()
                                c.send(json.dumps(member.res))
                                break
                            elif member.disconnected == True:
                                member.lastSeen = time.time()
                                member.disconnected = False
                                c.send(json.dumps(member.res))
                                break
                    else:
                        for member in self.captain.crew:
                            if member.res['id'] == obj["id"]:
                                member.getClue()
                                if obj['data']['key'] != "wait":
                                    self.addToClueList(member.res['id'], obj['data'])
                                    member.cluesSolved += 1
                                    member.totalCluesSolved += 1
                                    self.numClue += 1
                                    self.numMapClue += 1

                                c.send(json.dumps(member.res))
                                break

                    c.close()
                if self.numClue % 10 == 0:
                    print self.printPirates() + self.printProblemState()
                    self.restartNonRespondingPirates()
                self.verifyClues()

            print "YOU HAVE COMPLETED ONE MAP"
            self.killPoorPerformingPirates()
            self.numMap += 1


    def restartNonRespondingPirates(self):
        currentTime = time.time()
        for member in self.captain.crew:
            timeSince = int(currentTime - member.lastSeen)
            if timeSince > 25:
                print "Restarting non responding pirates..."
                member.disconnected = True
                member.startPirate(self.port)

    def killPoorPerformingPirates(self):
        print "Killing corrupt pirates..."
        killed = []
        for member in self.captain.crew:
            failureRate = 100.0 * (float(member.totalFailed) / float(member.totalCluesSolved + 1))
            print failureRate
            if (failureRate > 7.5):
                self.captain.remove(member.res['id'])  # send remove request to rummy
                killed.append(member)
                while True:
                    c, addr = self.s.accept()
                    obj = json.loads(str(c.recv(1024)))
                    if member.res['id'] == obj['id']:
                        member.res['finished'] = True
                        c.send(json.dumps(member.res))
                        c.close()
                        break
                    c.send(json.dumps(member.res))
                    c.close()

        self.captain.cleanUpMembers(killed)

        if len(killed) > 0:
            res = self.captain.add(len(killed))
            print res['message']
            crewids = res['data']
            self.captain.createMembers(crewids)

        self.startPirates()

    def verifyClues(self):
        if len(self.clueList) > self.verifyListSize or self.isDone():
            self.numClue = 0
            print " Verifying clueList..."
            rummyObj = self.captain.verify(self.clueList)
            self.clueList = []

            if 'finished' in rummyObj:
                for member in self.captain.crew:
                    c, addr = self.s.accept()
                    member.res['finished'] = True
                    obj = json.loads(str(c.recv(1024)))
                    c.send(json.dumps(member.res))
                    c.close()
                self.s.close()
                print "YOU COMPLETED THE PROBLEM"
                quit()
            elif rummyObj['status'] == "error":
                if 'data' in rummyObj:
                    data = rummyObj['data']
                    for clueError in data:
                        for member in self.captain.crew:
                            if member.res['id'] == clueError["id"]:
                                for error in clueError['data']:
                                    member.clues.append(error)
                                    member.statUpdateErrorClue()
                                    self.numMapClue -= 1
            for member in self.captain.crew:
                if len(member.clues) == 0 and member.res['data'] == 'wait':
                    member.paused = True

            print self.printPirates() + self.printProblemState()

    def startPirates(self):
        print "Rummy.startPirates called"
        for member in self.captain.crew:
            if member.connected == False:
                member.startPirate(self.port)
        print "Done starting pirates"

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

    def isAllDead(self):
        for member in self.captain.crew:
            if len(member.clues) > 0 or member.paused == False:
                return False
        return True

    def backspace(self, n):
        print('\r'*n)

    def printPirates(self):

        output = "+-----------------------------------------------------------------------+\n"
        output += "| ID\t\t\t\t\t| Conn\t| Solv\t| Left\t| Fail\t|\n"
        output += "|-----------------------------------------------------------------------|\n"
        for pirate in self.captain.crew:
            output += pirate.toString()
        output += "+-----------------------------------------------------------------------+\n"
        return output

    def printProblemState(self):

        clueSetPercentage = ((float(self.numClue) / float(self.verifyListSize)) * 100.0)
        clueSetDisplay = int(clueSetPercentage / 2.0)

        mapPercentage = ((float(self.numMapClue) / float(self.clueListSize)) * 100.0)
        mapDisplay = int(mapPercentage / 2.0)

        problemPercentage = (((float(self.numMap) / float(self.mapListSize)) * 100.0)+(mapPercentage/self.mapListSize))
        problemDisplay = int(problemPercentage / 2.0)

        output = "Problem completion (~): \n"
        output += str("{0:.1f}".format((problemPercentage if (problemPercentage < 100.0) else 100.0))) + " %\t["
        for x in range(0, problemDisplay):
            output += u'\u2588'
        for x in range(0, 50 - problemDisplay):
            output += " "
        output += "]\n"

        output += "Map completion (~):\n"
        output += str("{0:.1f}".format((mapPercentage if (mapPercentage < 100.0) else 100.0))) + " %\t["
        for x in range(0, mapDisplay):
            output += u'\u2588'
        for x in range(0, 50 - mapDisplay):
            output += " "
        output += "]\n"

        output += "Clue set completion:\n"
        output += str("{0:.1f}".format((clueSetPercentage if (clueSetPercentage < 100.0) else 100.0))) + " %\t["
        for x in range(0, clueSetDisplay):
            output += u'\u2588'
        for x in range(0, 50 - clueSetDisplay):
            output += " "
        output += "]\n"
        return output



quartermaster = Quartermaster()
quartermaster.listenDispatch()
