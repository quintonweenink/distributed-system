import json
import subprocess

execfile("member.py")

class Rummy:

    state = 0

    def __init__(self, crewSize):
        self.images = 20
        self.clues = {}
        self.crew = []
        self.crewSize = crewSize

        res = self.add(str(self.crewSize))
        print res['message']
        crewids = res['data']

        for id in crewids:
            self.crew.append(Member("", id, ""))

        for pirate in self.crew:
            print "{"
            pirate.toString()
            print "}"

        Rummy.state += 1

    def displayState(self):
        print "State: %d" % Rummy.empCount

    def displayEmployee(self):
        print "Name : ", self.name, ", Salary: ", self.salary

    def wake(self):
        print "Rummy.wake called"
        return self.reqRummy( ["-w"] )

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
        return self.reqRummy( ["-a", size] )

    def remove(self, pirates):
        print "Rummy.remove called"
        return self.reqRummy( ["-a", str(pirates)] )

    def shipout(self):
        print "Rummy.shipout called"
        return self.reqRummy( ["-s"] )

    def getClues(self):
        print "Rummy.getClues called"
        self.clues = self.reqRummy( ["-c"] )
        return self.clues

    def verify(self, clues):
        print "Rummy.verify called"
        return self.reqRummy( ["-v", str(clues)] )

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
# {
#     "status" :string, <-- success/error
#     "message" :string, <-- message of error/success
#     "data" :string-or-list,
#     "finished" :boolean <-- only true if all maps & clues have been solved and the treasure was found
# }
