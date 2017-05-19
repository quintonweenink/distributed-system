import json
import subprocess

execfile("member.py")

class Clue:
    def __init__(self, id, data):
        self.data = data
        self.id = id

class iRummy:

    def __init__(self, crewSize, port):
        print json.dumps(self.wake())
        print json.dumps(self.prepare())

        self.images = 20
        self.clues = {}
        self.crew = []
        self.crewSize = crewSize
        self.port = port

        res = self.add(str(self.crewSize))
        print res['message']
        crewids = res['data']

        self.createMembers(crewids)

        print json.dumps(self.shipout())

    def getPirateClues(self):
        res = self.getClues()
        print res['message']

        data = res['data']
        for pirate in data:
            for member in self.crew:
                if member.res['id'] == pirate["id"]:
                    member.clues = pirate["data"]

    def displayState(self):
        print "State: %d" % self.empCount

    def displayEmployee(self):
        print "Name : ", self.name, ", Salary: ", self.salary

    def wake(self):
        print "Rummy.wake called"
        return self.reqRummy( ["-w"] )

    def createMembers(self, crewids):
        print "Rummy.createMembers called with " + str(crewids)
        for id in crewids:
            self.crew.append(Member(id))

    def cleanUpMembers(self, killed):
        print "Rummy.cleanUpMembers called"
        for member in killed:
            self.crew.remove(member)

    def gather(self):
        print "Rummy.gather called"
        return self.reqRummy( ["-g"] )

    def unlock(self):
        print "Rummy.unlock called"
        return self.reqRummy( ["-u"] )

    def prepare(self):
        print "Rummy.prepare called"
        return self.reqRummy( ["-p"] )

    def add(self, size):
        print "Rummy.add called"
        return self.reqRummy( ["-a", str(size)] )

    def remove(self, pirates):
        print "Rummy.remove called"
        return self.reqRummy( ["-r", str(pirates)] )

    def shipout(self):
        print "Rummy.shipout called"
        return self.reqRummy( ["-s"] )

    def getClues(self):
        print "Rummy.getClues called"
        self.clues = self.reqRummy( ["-c"] )
        return self.clues

    def verify(self, clues):
        #print "Rummy.verify called"
        return self.reqRummy( ["-v", json.dumps(clues)] )

    def reqRummy(self, commands):
        args = ["python", "rummy.pyc"]

        for command in commands:
            args.append(command)

        output = subprocess.check_output(args).strip()
        obj = json.loads(str(output))
        return obj

    def printCrew(self):
        for pirate in self.crew:
            print "{"
            pirate.toString()
            print "}"