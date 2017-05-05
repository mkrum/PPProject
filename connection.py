
import pygame
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor


class Connection():

    def __init__(self, grid):
        self.grid = grid
        reactor.connectTCP("ash.campus.nd.edu", 40067, self.createClientCon())

    def createClientCon(self):
        cf = ClientFactory()
        self.connection = cf.myconn
        return cf

    def update(self, i, j, value):
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

    def dataReceived(self, data):
        self.queue.put(data)

    def q_callback(self, data):
        self.data_connection.transport.write(data)
        self.queue.get().addCallback(self.q_callback)



class ClientFactory(Factory):
    def __init__(self):
        self.myconn = ClientConnection()
        self.myconn.ready = False

    def buildProtocol(self, addr):
        return self.myconn


