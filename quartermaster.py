#!/usr/bin/python

import socket
import json
import sys
import subprocess

execfile("irummy.py")

# Master
class Quartermaster:

    state = 0

    def __init__(self, crewSize):
        self.startport = 12345  # Reserve a port for your service.
        self.crewSize = crewSize
        self.clueList = []
        self.verifyListSize = 199
        self.mapListSize = 20.0
        self.clueListSize = 1000.0

        print "========== QUARTERMASTER ======="

        print "ARRGG.. STARTING "
        print "PORT: ", self.port
        print "Crew Size: ", self.crewSize

        print "================================"
        print ""

        self.captain = iRummy(crewSize, self.startport)

    def listenDispatch(self):

        numClue = 0
        numMap = 0
        outputChars = 0
        numMapClue = 0
        self.backspace(outputChars)
        output = self.printPirates(numMap, numClue, numMapClue)
        print(output)
        outputChars = len(output)

        while True:
            self.captain.getPirateClues()
            numMapClue = 0


            for member in self.captain.crew:
                member.paused = False
                member.cluesSolved = 0
                member.failed = 0

            while not self.isAllDead() or len(self.clueList) > 0:

                # RECEIVE AND DISPATCH THE CLUES
                if not self.isAllDead():
                    c, addr = self.s.accept()  # Establish connection with client.
                    obj = json.loads(str(c.recv(1024)))

                    # print json.dumps(obj)
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
                                if obj['data']['key'] != "wait":
                                    self.addToClueList(member.res['id'], obj['data'])
                                    member.cluesSolved += 1
                                    member.totalCluesSolved += 1
                                    numClue += 1
                                    numMapClue += 1

                                c.send(json.dumps(member.res))
                                break

                    c.close()  # Close the connection

                self.backspace(outputChars)
                output = self.printPirates(numMap, numClue, numMapClue)
                print(output)
                outputChars = len(output)


                # VERIFY THE SOLVED CLUES
                if len(self.clueList) > self.verifyListSize or self.isDone():
                    numClue = 0
                    outputChars = 0
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

                        sys.exit("YOU COMPLETED THE PROBLEM")
                    elif rummyObj['status'] == "error":
                        if 'data' in rummyObj:
                            data = rummyObj['data']
                            for clueError in data:
                                for member in self.captain.crew:
                                    if member.res['id'] == clueError["id"]:
                                        for error in clueError['data']:
                                            member.clues.append(error)
                                            member.cluesSolved -= 1
                                            member.totalCluesSolved -= 1
                                            member.totalFailed += 1
                                            member.failed += 1
                                            numMapClue -= 1
                    for member in self.captain.crew:
                        if len(member.clues) == 0 and member.res['data'] == 'wait':
                            member.paused = True

                    self.backspace(outputChars)
                    output = self.printPirates(numMap, numClue, numMapClue)
                    print(output)
                    outputChars = len(output)

            print "YOU HAVE COMPLETED ONE MAP"
            numMap += 1

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

    def startPirates(self):
        print "Rummy.startPirates called"
        for i in range(0, self.crewSize):
            self.startPirate()
        print "Done starting pirates"

    def backspace(self, n):
        print('\r'*n)

    def printPirates(self, m, i, mc):
        output = "+-----------------------------------------------------------------------+\n"
        output += "| ID\t\t\t\t\t| Conn\t| Solv\t| Left\t| Fail\t|\n"
        output += "|-----------------------------------------------------------------------|\n"
        for pirate in self.captain.crew:
            output += pirate.toString()
        output += "+-----------------------------------------------------------------------+\n"

        clueSetPercentage = ((float(i) / float(self.verifyListSize)) * 100.0)
        clueSetDisplay = int(clueSetPercentage / 2.0)

        mapPercentage = ((float(mc) / float(self.clueListSize)) * 100.0)
        mapDisplay = int(mapPercentage / 2.0)

        problemPercentage = (((float(m) / float(self.mapListSize)) * 100.0)+(mapPercentage/self.mapListSize))
        problemDisplay = int(problemPercentage / 2.0)

        output += "Problem completion (~): \n"
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



quartermaster = Quartermaster(10)
quartermaster.listenDispatch()
