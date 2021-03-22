from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import threading

class Server(DatagramProtocol):
    def __init__(self):
        self.client = set()
        reactor.callInThread(self.allMember)

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode("utf-8")
        if datagram == "ready":
            #go to new line for every client
            data = "ok"
            self.transport.write(data.encode("utf-8"), addr)
            self.client.add(addr)
            #print(addr, 'is connection')
        elif datagram == 'out':
            self.client.remove(addr)
            #text = str(addr) + " is out"
            #print(text)
        else:
            print(datagram)

    def allMember(self):
        text = "Choose a client from these\n"
        for x in self.client:
            text += str(x) + '\n'
        
        for x in self.client:
            self.transport.write(text.encode("utf-8"), (x[0], 9999))

        threading.Timer(5.0, self.allMember).start()

if __name__ == '__main__':
    #Server need to fix port
    serverPort = 9999
    reactor.listenUDP(serverPort, Server())
    reactor.run()