class Member:

    def __init__(self, id):
        self.connected = False;
        self.clues = []
        self.cluesSolved = 0
        self.failed = 0

        self.res = {
            "status": "",  # string, <-- success/error
            "message": "",  # string, <-- message of error/success
            "data": "",  # string-or-list,
            "id": id,
            "finished": False,  # boolean <-- only true if all maps & clues have been solved and the treasure was found
        }

    def toString(self):
        print ("{")
        print ("    connected:" + str(self.connected))
        print ("    Clues solved:" + str(self.cluesSolved))
        print ("    Clues left:" + str(len(self.clues)))
        print ("    Id:" + str(self.res['id']))
        print ("    Failure rate:" + str((float(self.failed) / float(self.cluesSolved))))
        print ("}")

    def getClue(self):
        if len(self.clues) >= 1:
            self.res['data'] = self.clues.pop()
        else:
            self.res['data'] = "wait"
