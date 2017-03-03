#!/usr/bin/python

import socket               # Import socket module
import json
import hashlib
import sys
import time



class Pirate:

    def __init__(self):
        self.s = 0
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12359    # Reserve a port for your service.
        self.clue = "No clue provided"
        self.clueid = -1

        self.res = {
            "status": "",  # string, <-- success/error
            "message": "",  # string, <-- message of error/success
            "data": "",  # string-or-list,
            "id": -1,
            "finished": False,  # boolean <-- only true if all maps & clues have been solved and the treasure was found
        }

    def toString(self):
        print ("    Id:" + str(self.id))

    def communicate(self):
        self.s = socket.socket()  # Create a socket object
        self.s.connect((self.host, self.port))
        self.res['data'] = {
            'key':self.clue,
            'id':self.clueid
        }

        self.s.send(json.dumps(self.res))

        obj = json.loads(str(self.s.recv(4096)))


        if self.res['id'] == -1:
            self.res['id'] = obj['id']
            self.clue = obj['data']['data']
            self.clueid = obj['data']['id']
        elif obj['data'] == "wait":
            time.sleep(1)
            self.clue = "wait"
            self.res["data"] = "wait"
        elif obj['finished'] == True:
            sys.exit("This pirate is done")
        else:
            self.clue = obj['data']['data']
            self.clueid = obj['data']['id']

        self.s.close()

    def listen(self):
        if self.clue != "wait":
            self.solveTheClue()
        self.communicate()



    def solveTheClue(self):
        self.digInTheSand()
        self.searchTheRiver()
        self.crawlIntoTheCave()

        self.clue = hashlib.md5(self.clue).hexdigest().upper()

        self.res['finished'] = True

    def digInTheSand(self):
        for i in range(0, 100):
            self.shovel()
        for i in range(0, 200):
            self.bucket()
        for i in range(0, 100):
            self.shovel()


    def searchTheRiver(self):
        for i in range(0, 200):
            self.bucket()

    def crawlIntoTheCave(self):
        for i in range(0, 200):
            self.rope()
        for i in range(0, 100):
            self.torch()

    def shovel(self):
        self.clue = ''.join(sorted(self.clue))
        if self.clue[0].isdigit():
            self.clue += '0A2B3C'
        else:
            self.clue += '1B2C3D'
        self.clue = self.clue[1:]

    def rope(self):
        res = ""
        for c in self.clue:
            if c.isdigit():
                digit = int(c) % 3
                if digit == 0:
                    res += '5'
                elif digit == 1:
                    res += 'A'
                elif digit == 2:
                    res += 'B'
                else:
                    res += c
            else:
                hex = (ord(c) - 65) % 5
                if hex == 0:
                    res += 'C'
                elif hex == 1:
                    res += '1'
                elif hex == 2:
                    res += '2'
                else:
                    res += c

        self.clue = res

    def torch(self):
        x = sum(int(x) for x in self.clue if x.isdigit())
        if x < 100:
            x = x ** 2
        self.clue = str(x)
        if len(self.clue) < 10:
            self.clue = "F9E8D7" + self.clue[1:]
        else:
            self.clue = self.clue[6:] + "A1B2C3"

    def bucket(self):
        res = ""
        for c in self.clue:
            if c.isdigit():
                if int(c) > 5:
                    res += str(int(c) - 2)
                else:
                    res += str(int(c) * 2)
            else:
                res += c
        self.clue = res




pirate = Pirate()

pirate.communicate()
while(True):
    pirate.listen()