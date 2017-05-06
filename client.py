import pygame
from gamespace import GameSpace
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.defer import DeferredQueue
from twisted.python import log
import sys
log.startLogging(sys.stdout)

''' Client Connection '''

class ClientConnection(Protocol):
    def __init__(self, gs):
        self.queue = DeferredQueue()
        self.gs = gs
        self.gs.connection = self
        self.startForwarding()

    def connectionMade(self):
        print('client connection made')
    
    def update(self, i, j, value):
        self.transport.write('{} {} {}'.format(i, j, value))

    def dataReceived(self, data):
        # print('home client connection got data: {}'.format(data))
        self.queue.put(data)

    def forwardData(self, data):
        if data == 'start the game':
            print('starting game')
            self.gs.started = True
        elif self.gs.started:
            print('data: {}'.format(data))
        else:
            print('data: {}'.format(data))
        self.queue.get().addCallback(self.forwardData)

    #def dataReceived(self, data):
    #    # print('home client connection got data: {}'.format(data))
    #    self.queue.put(data)

    #def forwardData(self, data):
    #    self.queue.get().addCallback(self.forwardData)
    def startForwarding(self):
        self.queue.get().addCallback(self.forwardData)

    def connectionLost(self, reason):
        if reactor.running:
            reactor.stop()


class ClientConnectionFactory(ClientFactory):
    def __init__(self, gs):
        self.conn = ClientConnection(gs)

    def buildProtocol(self, addr):
        return self.conn

def errorHandler(reason):
    if reactor.running:
        reactor.stop()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()

    gs_tick = LoopingCall(gs.game_space_tick)
    gs_tick.start((1.0/60.0)).addErrback(errorHandler)

    clientConnFactory = ClientConnectionFactory(gs)
    reactor.connectTCP("newt.campus.nd.edu", 40067, clientConnFactory)
    reactor.run()
