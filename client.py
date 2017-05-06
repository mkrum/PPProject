import pygame
from gamespace import GameSpace
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
# from twisted.internet.defer import DeferredQueue
from twisted.python import log
import sys
log.startLogging(sys.stdout)

#class Connection():
#
#    def __init__(self, grid):
#        self.grid = grid
#        reactor.connectTCP("ash.campus.nd.edu", 40067, self.createClientCon())
#        reactor.run()
#        print("connect")
#
#    def createClientCon(self):
#        cf = clientFactory()
#        self.connection = cf.myconn
#        return cf
#
#    def update(self, i, j, value):
#        #just for now
#        if self.connection.ready:
#           self.connection.transport.write("%s %s %s" % (str(i), str(j), str(value)))

''' Client Connection '''

class ClientConnection(Protocol):
    def __init__(self, gs):
        # self.queue = DeferredQueue()
        self.gs = gs
        self.gs.connection = self
        # startForwarding()

    def connectionMade(self):
        print('client connection made')
    
    def dataReceived(self, data):
        if data == 'start the game':
            print('starting game')
            self.gs.started = True
        elif self.gs.started:
            print('data: {}'.format(data))

    def update(self, i, j, value):
        pass
        #self.transport.write('{} {} {}'.format(i, j, value))

    #def dataReceived(self, data):
    #    # print('home client connection got data: {}'.format(data))
    #    self.queue.put(data)

    #def forwardData(self, data):
    #    self.queue.get().addCallback(self.forwardData)

    #def startForwarding(self):
    #    self.queue.get().addCallback(self.forwardData)


class ClientConnectionFactory(ClientFactory):
    def __init__(self, gs):
        self.conn = ClientConnection(gs)

    def buildProtocol(self, addr):
        return self.conn

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()

    gs_tick = LoopingCall(gs.game_space_tick)
    gs_tick.start((1.0/60.0)).addErrback(log.err)

    clientConnFactory = ClientConnectionFactory(gs)
    #reactor.connectTCP("newt.campus.nd.edu", 40067, clientConnFactory)
    reactor.run()
