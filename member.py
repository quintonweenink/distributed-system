import socket
import subprocess

class Member:

    def __init__(self, id, port):
        # Control variables
        self.connected = False
        self.clues = []
        self.cluesSolved = 0
        self.totalCluesSolved = 0
        self.failed = 0
        self.totalFailed = 0
        self.paused = False

        # Connection variables
        self.s = {}
        self.host = socket.gethostname()  # Get local machine name
        self.port = port  # Reserve a port for your service.

        # Messaging object
        self.res = {
            "status": "",  # string, <-- success/error
            "message": "",  # string, <-- message of error/success
            "data": "",  # string-or-list,
            "id": id,
            "finished": False,  # boolean <-- only true if all maps & clues have been solved and the treasure was found
        }

        # Open the connection
        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to the port
        self.s.listen(20)  # Now wait for client connection.

        self.startPirate()

    def toString(self):
        failureRate = "{0:.1f}".format(100.0 * (float(self.totalFailed) / float(self.totalCluesSolved + 1)))
        return "| "+str(self.res['id'])+"\t| "+str(self.connected)+"\t| "+str(self.cluesSolved)+"\t| "+str(len(self.clues))+"\t| "+ failureRate + "%\t|\n"


    def getClue(self):
        if len(self.clues) > 0:
            self.res['data'] = self.clues.pop()
        else:
            self.res['data'] = "wait"

    def startPirate(self):
        print "Rummy.startPirate called"
        args = ["./pirate.py", str(self.port), "&"]
        subprocess.Popen(args)
