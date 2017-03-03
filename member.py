class Member:

    def __init__(self, id):
        self.connected = False;
        self.clues = []
        self.cluesSolved = 0

        self.res = {
            "status": "",  # string, <-- success/error
            "message": "",  # string, <-- message of error/success
            "data": "",  # string-or-list,
            "id": id,
            "finished": False,  # boolean <-- only true if all maps & clues have been solved and the treasure was found
        }

    def toString(self):
        print ("    connected:" + str(self.connected))
        print ("    Clues solved:" + str(self.cluesSolved))
        print ("    Clues left:" + str(len(self.clues)))
        print ("    Id:" + str(self.res['id']))
