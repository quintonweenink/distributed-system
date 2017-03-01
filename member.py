class Member:

    def __init__(self, connection, id, addr):
        self.connection = connection
        self.id = id
        self.addr = addr

        self.res = {
            "status": "",  # string, <-- success/error
            "message": "",  # string, <-- message of error/success
            "data": "40938FC0CB3F48B98C7546AD05CC7434",  # string-or-list,
            "finished": False,  # boolean <-- only true if all maps & clues have been solved and the treasure was found
        }

    def toString(self):
        print ("    Connection:" + str(self.connection))
        print ("    Id:" + str(self.id))
        print ("    Addr:" + str(self.addr))