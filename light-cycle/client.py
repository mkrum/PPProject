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

    # player has joined the game
    def connectionMade(self):
        print('client connection made')
    
    # send update over connection
    def update(self, data):
        self.transport.write('{}'.format(str(data)))

    # put the data on the queue
    def dataReceived(self, data):
        self.queue.put(data)

    # handle the data that was received
    def forwardData(self, data):
        if 'start the game' in data:
            # set which connection is which player and start the game
            _, num = data.split(',', 1)
            self.gs.set_players(num)
            self.gs.started = True
        elif self.gs.started and not self.gs.finished:
            print('data: {}'.format(data))
            # this player won
            if 'win' in data:
                self.gs.game_over_screen('win')

            # this player lost
            elif 'lose' in data:
                self.gs.game_over_screen('lose')

            # other player disconnected
            elif 'connection lost' in data:
                self.gs.text_screen('Other player has left. Click to quit.')

            # a move has been sent, update oppenent's position
            elif 'up' in data or 'down' in data or 'left' in data or 'right' in data:
                self.gs.opponent.receive_move_location(data, gs.grid.data)
        
        # re-add itself as callback
        self.queue.get().addCallback(self.forwardData)

    # add the callback to the deferred queue
    def startForwarding(self):
        self.queue.get().addCallback(self.forwardData)

    # stop running when the connection is lost
    def connectionLost(self, reason):
        if reactor.running:
            reactor.stop()


class ClientConnectionFactory(ClientFactory):
    def __init__(self, gs):
        self.conn = ClientConnection(gs)

    def buildProtocol(self, addr):
        return self.conn

# quit on errors
def errorHandler(reason):
    if reactor.running:
        reactor.stop()

if __name__ == '__main__':
    # initialize gamespace
    gs = GameSpace()
    gs.main()
    
    # run game_space_tick at 60 fps
    # http://stackoverflow.com/questions/8381850/combining-pygame-and-twisted
    # this is an alternative to using clock.tick(60) in pygame
    gs_tick = LoopingCall(gs.game_space_tick)
    gs_tick.start((1.0/60.0)).addErrback(errorHandler)

    # connect to server
    clientConnFactory = ClientConnectionFactory(gs)
    reactor.connectTCP("newt.campus.nd.edu", 40067, clientConnFactory)
    reactor.run()
