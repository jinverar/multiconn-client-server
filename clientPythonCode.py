from clientApp import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QIcon

from ConnectorDialog import Connector_Dialog
import platform

#python selectors
# ref for selectors https://docs.python.org/3/library/selectors.html
#This module allows high-level and efficient I/O multiplexing, built upon the select module primitives.
import selectors
import socket

#python TYPES This module defines utility functions to assist in dynamic creation of new types.
#It also defines names for some object types that are used by the standard Python interpreter, but not exposed as builtins like int or str are.
#Finally, it provides some additional type-related utility classes and functions that are not fundamental enough to be builtins.
import types


#class selectors.DefaultSelector, The default selector class, using the most efficient implementation available on the current platform. 
##This should be the default choice for most users.
#put the DefaultSelector into a variable called "sel"
sel = selectors.DefaultSelector()
connid = []
server_addr = []

#below is my commands function. The user will enter commands and receive responses back. 
def commands():
    import os
    # below is the code to do STDOUT STDERR for events_lineEditTab1
    command = str(ui.console_lineEdit.text())
    stdouterr = os.popen(command).read()
    ui.console_textEdit.setText(stdouterr)

    if 'exit' in command:
        app.exit()

    if 'help' in command:
        ui.console_textEdit.setText("[**] below are the main window help commands ")
        ui.console_textEdit.append("[+] Command options: ")
        ui.console_textEdit.append("[+] connect ====== > connect to the experimantal server")
        ui.console_textEdit.append("[+] check ====== > check for connected clients")
        ui.console_textEdit.append("[+] close ====== > disconnect from the server")
        ui.console_textEdit.append("[+] getenv ====== > send the environment back to the server, //not working")

    if 'getenv' in command:
        sock.send( "[+] Platform Is " + platform.platform()) 

    if 'close' in command:
        sel.close()
        ui.console_textEdit.append(" [**] the connection id %s to %s is closed" % (connid, server_addr))

    if 'check' in command:
        #--------------------------------------------------------------------------------------------------
        #clients = {'sip.voidptr object at 0x00000122031B2AD0' : 'PyQt5.QtNetwork.QTcpSocket object at 0x00000122031C53A8', 'sip.voidptr object at 0x00000122031B2B48': 'PyQt5.QtNetwork.QTcpSocket object at 0x00000122033D44C8'}
        #-----------------------------------------------------------------------------------------------------
        #ui.console_textEdit.append(" [**] the connection ids are %s" % connid)
        ui.console_textEdit.append(" [**] the selector objects are %s" % sel)
        ui.console_textEdit.append(" [**] the keys are %s" % sel.get_key)
        ui.console_textEdit.append(" [**] the map of clients are %s" % sel.get_map)
        ui.console_textEdit.append(" [**] the select values are %s" % sel.select)
        #ui.console_textEdit.append(" [**] client has connected and the socket objects are %s" % ui.conn)



    if 'connect' in command:
        Dialog = QtWidgets.QDialog()
        Connector_ui = Connector_Dialog()
        Connector_ui.setupUi(Dialog)
        Dialog.show()
        #Dialog.exec_()
        
        rsp = Dialog.exec_()
        
        if rsp == QtWidgets.QDialog.Accepted:
            address = Connector_ui.ip_address_lineEdit.text()
            port = Connector_ui.port_lineEdit.text()
            num_conns = Connector_ui.num_conns_lineEdit.text()
            num_conns = int(num_conns)
            start_connections(address, port, num_conns)
            try:
                while True:
                    events = sel.select(timeout=1)
                    if events:
                        for key, mask in events:
                            service_connection(key, mask)
                    # Check for a socket being monitored to continue.
                    if not sel.get_map():
                        break
            except KeyboardInterrupt:
                print("caught keyboard interrupt, exiting")
            finally:
                sel.close()
              
        else:
            ui.console_textEdit.append("you have quit the connector dialog")


messages = [b'Message 1 from client.', b'Message 2 from client.']
#num_conns is read from the command-line, which is the number of connections to create to the server. Just like the server, each socket is set to non-blocking mode.
def start_connections(address, port, num_conns):
    #add the address and port to the server_addr so we can use this to connect
    server_addr = (address, int(port))
    #create a for loop to increase the number of connections each time a client connects. 
    for i in range(0, num_conns):
        #increase the connid by 1 each time
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        ui.console_textEdit.append(" [**] connected and the connection id is %s to %s" % (connid, server_addr))
        #create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #set the socket to non blocking
        sock.setblocking(False)
        #if there is an error then connect_ex() returns an error indicator, errno.EINPROGRESS, instead of raising an exception while the connection is in progress. 
        #Once the connection is completed, the socket is ready for reading and writing and is returned as such by select().
        #connect the socket to the server address
        sock.connect_ex(server_addr)
        #he following, events is a bitwise mask indicating which I/O events should be waited for on a given file object
        #A mask defines which bits you want to keep, and which bits you want to clear.
        #Masking is the act of applying a mask to a value. This is accomplished by doing, 
        #Bitwise ANDing in order to extract a subset of the bits in the value
        #Bitwise ORing in order to set a subset of the bits in the value
        #Bitwise XORing in order to toggle a subset of the bits in the value
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        #After the socket is setup, the data we want stored with the socket is created using the class types.SimpleNamespace. 
        #The messages the client will send to the server are copied using list(messages) since each connection will call socket.send() and modify the list. 
        #Everything needed to keep track of what the client needs to send, has sent and received, and the total number of bytes in the messages is stored in the object data.

        #class types.SimpleNamespace, A simple object subclass that provides attribute access to its namespace, as well as a meaningful repr.Unlike object, 
        #with SimpleNamespace you can add and remove attributes. If a SimpleNamespace object is initialized with keyword arguments, 
        #those are directly added to the underlying namespace.

        # put type simple namespace into data and check the connid, if the connid is true then send the message if receive total is 0 check the list.
        #data might be a named selector variable, Optional opaque data associated to this file object: for example, this could be used to store a per-client session ID.
        data = types.SimpleNamespace(connid=connid,msg_total=sum(len(m) for m in messages),recv_total=0,messages=list(messages),outb=b'')

        #call the sel variable and register the selector with the sock.
        #Events that must be waited for on this file object.
        #data must equal data
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    #File object registered.
    #key is the SelectorKey instance corresponding to a ready file object. events is a bitmask of events ready on this file object.
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            #It keeps track of the number of bytes it’s received from the server so it can close its side of the connection. 
            #When the server detects this, it closes its side of the connection too.
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]



if __name__ == "__main__":
    import sys
    import os
    import socket
    import time
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)


    ui.console_lineEdit.setObjectName("events_lineEdit")
    ui.console_lineEdit.setPlaceholderText(" -> Cl13nt cmdz, type help to get menu and then connect to server with 'connect' ")
    ui.console_lineEdit.setStyleSheet("QLineEdit { background-color: black; color: white; font-size: 12px; font-weight: bold; }")
    ui.console_lineEdit.returnPressed.connect(commands)
    ui.console_lineEdit.returnPressed.connect(ui.console_lineEdit.clear)



    MainWindow.show()
    sys.exit(app.exec_())
