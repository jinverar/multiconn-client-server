import socket
import selectors
import types
sel = selectors.DefaultSelector()

host = '192.168.1.183'  # The server's hostname or IP address
port = 12345       # The port used by the server
# ...
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False) #lsock.setblocking(False) to configure the socket in non-blocking mode

#sel.register() registers the socket to be monitored with sel.select() 
##for the events you’re interested in. For the listening socket, we want read events: selectors.EVENT_READ.
sel.register(lsock, selectors.EVENT_READ, data=None)

#The accept wrapper: Since the listening socket was registered for the event selectors.EVENT_READ, it should be ready to read. 
#We call sock.accept() and then immediately call conn.setblocking(False) to put the socket in non-blocking mode.
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    #we create an object to hold the data we want included along with the socket using the class types.SimpleNamespace. 
    #Since we want to know when the client connection is ready for reading and writing, both of those events are set using the following:
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    #The events mask, socket, and data objects are then passed to sel.register()
    sel.register(conn, events, data=data)

#This is the heart of the simple multi-connection server. 
#key is the namedtuple returned from select() that contains the socket object (fileobj) and data object. 
#mask contains the events that are ready.
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        #If the socket is ready for reading, then mask & selectors.EVENT_READ is true, and sock.recv() is called. 
        #Any data that’s read is appended to data.outb so it can be sent later.
        #Note the else: block if no data is received:
        if recv_data:
            data.outb += recv_data
        #This means that the client has closed their socket, so the server should too. But don’t forget to first call sel.unregister() so it’s no longer monitored by select().
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            #sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            #When the socket is ready for writing, which should always be the case for a healthy socket,
            #any received data stored in data.outb is echoed to the client using sock.send(). 
            #The bytes sent are then removed from the send buffer:
            data.outb = data.outb[sent:]

while True:
    #sel.select(timeout=None) blocks until there are sockets ready for I/O
    #It returns a list of (key, events) tuples, one for each socket. 
    #key is a SelectorKey namedtuple that contains a fileobj attribute. 
    #key.fileobj is the socket object, and mask is an event mask of the operations that are ready
    events = sel.select(timeout=None) 
    for key, mask in events:
        #If key.data is None, then we know it’s from the listening socket and we need to accept() the connection. 
        #We’ll call our own accept() wrapper function to get the new socket object and register it with the selector.
        if key.data is None:
            accept_wrapper(key.fileobj)

        #If key.data is not None, then we know it’s a client socket that’s already been accepted, and we need to service it. 
        #service_connection() is then called and passed key and mask, which contains everything we need to operate on the socket.
        else:
            service_connection(key, mask)




