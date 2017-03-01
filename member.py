class Member:

    state = 0

    def __init__(self, connection, id, addr):
        self.connection = connection
        self.id = id
        self.addr = addr
        Member.state += 1

    def toString(self):
        print ("    Connection:" + str(self.connection))
        print ("    Id:" + str(self.id))
        print ("    Addr:" + str(self.addr))