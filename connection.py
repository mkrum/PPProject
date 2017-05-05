
import pygame
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor


class Connection():

    def __init__(self, grid):
        self.grid = grid
        reactor.connectTCP("ash.campus.nd.edu", 40067, self.createClientCon())
        reactor.run()
        print("connect")

    def createClientCon(self):
        cf = clientFactory()
        self.connection = cf.myconn
        return cf

    def update(self, i, j, value):
        #just for now
        if self.connection.ready:
            self.connection.transport.write("%s %s %s" % (str(i), str(j), str(value)))


#Client
class ClientConnection(Protocol):

    def connectionMade(self):
        self.ready = True

    def createDataCon(self):
        data_factory = DataFactory()
        self.data_connection = data_factory.myconn
        self.data_connection.service_connection = self
        return data_factory





class clientFactory(ClientFactory):
    def __init__(self):
        self.myconn = ClientConnection()
        self.myconn.ready = False

    def buildProtocol(self, addr):
        return self.myconn


