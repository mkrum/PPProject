from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.python import log
import sys
log.startLogging(sys.stdout)

'''
    Useful resource:
    http://twistedmatrix.com/documents/13.0.0/core/howto/servers.html
'''

''' Client Connection '''

class ClientConnection(Protocol):
    def __init__(self, conns):
        self.queue = DeferredQueue()
        self.startForwarding()
        self.conns = conns

    # client has connected to server
    def connectionMade(self):
        # limit the number of client connections to 2
        if len(self.conns) >= 2:
            self.transport.write('two players are already playing')
            self.transport.loseConnection()
            return

        if not self.conns:
            # first client connection
            self.num = 0
        else:
            # second client connection
            self.num = 1

        print('player {} connected'.format(self.num))
        self.conns.append(self)
        
        # both players are connected
        if len(self.conns) == 2:
            for c in self.conns:
                c.transport.write('start the game,{}'.format(c.num))

    def connectionLost(self, reason):
        if self in self.conns:
            # remove this connection
            self.conns.remove(self)
            print('connection lost')
            print('number of connections: {}'.format(len(self.conns)))

            # notify the other connection if there is one
            # that their opponent left
            if self.conns:
                self.conns[0].transport.write('connection lost')

    def dataReceived(self, data):
        self.queue.put(data)

    def forwardData(self, data):
        self.writeOther(data)
        self.queue.get().addCallback(self.forwardData)

    def startForwarding(self):
        self.queue.get().addCallback(self.forwardData)
    
    def writeOther(self, data):
        # 0 writes to 1 and 1 writes to 0
        if len(self.conns) == 2:
            other = 0 if self.num else 1
            self.conns[other].transport.write(data)


class ClientConnectionFactory(ClientFactory):
    def __init__(self):
        # list of clients connected to this server
        self.conns = []

    def buildProtocol(self, addr):
        return ClientConnection(self.conns)

# start listening on port 40067
clientFactory = ClientConnectionFactory()
reactor.listenTCP(40067, clientFactory)

reactor.run()
