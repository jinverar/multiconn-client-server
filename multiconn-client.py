#!/usr/bin/env python3

import sys
import socket
import selectors
import types


#messages = [b"Message 1 from client.", b"Message 2 from client."]
#sel = selectors.DefaultSelector()

class ClientCommunicator(object):
    
    def __init__(self, name):
        self.name = name
        self.Messges = [b"Message 1 from client.", b"Message 2 from client."]
        self.Selctr = selectors.DefaultSelector()

    #so you can type   class.propertyname = value
    #or you can type  value = class.propertyname

    @property
    def Messges(self):
        return self.__messges

    @Messges.setter
    def Messges(self, value):
        self.__messges = value

    @property
    def Selctr(self):
        return self.__selectr

    @Selctr.setter
    def Selctr(self, value):
        self.__selectr = value

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, value):
        self.__name = value



    def start_connections(self, host, port, num_conns):
        server_addr = (host, port)
        for i in range(0, num_conns):
            connid = i + 1
            print("starting connection", connid, "to", server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            MyMsgs = self.Messges
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in MyMsgs),
                recv_total=0,
                MyMsgs=list(MyMsgs),
                outb=b"",
            )
            self.Selctr.register(sock, events, data=data)
    
    
    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data), "from connection", data.connid)
                data.recv_total += len(recv_data)
            #if not recv_data or data.recv_total == data.msg_total:
            #    print("closing connection", data.connid)
            #    sel.unregister(sock)
            #    sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.MyMsgs:
                data.outb = data.MyMsgs.pop(0)
            if data.outb:
                print("sending", repr(data.outb), "to connection", data.connid)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
    
    

    

    def Starter(self):
        if len(sys.argv) != 4:
            print("usage:", sys.argv[0], "<host> <port> <num_connections>")
            sys.exit(1)
        host, port, num_conns = sys.argv[1:4]
        self.start_connections(host, int(port), int(num_conns))
        #the  closeConnct is just a boolean Flag
        #could have called it Doodles
        closeConnct = False
        try:
            while True:
                command = input("-> " )
                if 'close' in command:
                    #closeConnct = True
                    self.Selctr.close()
                events = self.Selctr.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.Selctr.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
            
        if closeConnct:
            sel.shutdown()
            sel.close()
        
    #finally:
    #    sel.close()

    
if __name__ == "__main__":
    main = ClientCommunicator('name')
    main.Starter()
