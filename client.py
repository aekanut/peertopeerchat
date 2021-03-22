#protocol for udp connection
from twisted.internet.protocol import DatagramProtocol
#The reactor is the Twisted event loop within Twisted 
from twisted.internet import reactor
#random int
from random import randint

#Parent class is DatagramProtocol
#Child class is Client  
class Client(DatagramProtocol):
    def __init__(self, serverHost, host, port):
        if host == "localhost":
            host = "127.0.0.1"
        
        if serverHost == 'localhost':
            serverHost = "127.0.0.1"

        self.id = host, port
        self.address = None
        self.server = serverHost, 9999
        print("Working on id:", self.id)

    def sendOneMessage(self, text, des):
        self.transport.write(text.encode("utf-8"), des)
    #datagram is the bytes received from the transport
    #addr is tuple of source of datagram
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode("utf-8")
        if addr == self.server:  
            print("status", datagram, "\n")
            self.address = input("Write host:"), int(input("Write port:"))
            print("You can chat now!")
            reactor.callInThread(self.sendMessage)
        else:
            print(addr, ":", datagram)
    
    def startProtocol(self):
        self.sendOneMessage("ready", self.server)
    
    def doStop(self):
        self.sendOneMessage("out", self.server)
        outText = " out!"
        self.sendOneMessage(outText, self.address)

    def sendMessage(self):
        while True:
            self.sendOneMessage(input(""), self.address)

if __name__ == '__main__':
    #this is dynamic port
    port = randint(49152, 65535)
    host = input('Write your host: ')
    serverHost = input('Write your server host: ')
    reactor.listenUDP(port, Client(serverHost ,host, port))
    reactor.run()
    