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
    
    def update(self, move):
        self.transport.write('{}'.format(move))

    def dataReceived(self, data):
        self.queue.put(data)

    def forwardData(self, data):
        if 'start the game' in data:
            _, num = data.split(',', 1)
            self.gs.set_players(num)
            self.gs.started = True
        elif self.gs.started:
            print('data: {}'.format(data))
            if 'win' in data or 'lose' in data:
                self.gs.game_over_screen(data)
            else:
                self.gs.opponent.receive_move_location(data, gs.grid.data)
        self.queue.get().addCallback(self.forwardData)

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
    print(reason)
    if reactor.running:
        reactor.stop()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
        
    gs_tick = LoopingCall(gs.game_space_tick)
    gs_tick.start((1.0/60.0)).addErrback(errorHandler)

    clientConnFactory = ClientConnectionFactory(gs)
    reactor.connectTCP("newt.campus.nd.edu", 40071, clientConnFactory)
    reactor.run()
