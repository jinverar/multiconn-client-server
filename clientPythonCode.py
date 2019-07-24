from clientApp import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QIcon

from ConnectorDialog import Connector_Dialog



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
            numm = Connector_ui.num_conns_lineEdit.text()
              
        else:
            ui.console_textEdit.append("you have quit the connector dialog")



#num_conns is read from the command-line, which is the number of connections to create to the server. Just like the server, each socket is set to non-blocking mode.
def start_connections(address, port, num_conns):
    server_addr = (ui.address, ui.port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        #connect_ex() is used instead of connect() since connect() would immediately raise a BlockingIOError exception. 
        #connect_ex() initially returns an error indicator, errno.EINPROGRESS, instead of raising an exception while the connection is in progress. 
        #Once the connection is completed, the socket is ready for reading and writing and is returned as such by select().
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        #After the socket is setup, the data we want stored with the socket is created using the class types.SimpleNamespace. 
        #The messages the client will send to the server are copied using list(messages) since each connection will call socket.send() and modify the list. 
        #Everything needed to keep track of what the client needs to send, has sent and received, and the total number of bytes in the messages is stored in the object data.
        data = types.SimpleNamespace(connid=connid,msg_total=sum(len(m) for m in messages),recv_total=0,messages=list(messages),outb=b'')
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            #It keeps track of the number of bytes it’s received from the server so it can close its side of the connection. 
            #When the server detects this, it closes its side of the connection too.
            data.recv_total += len(recv_data)
        #if not recv_data or data.recv_total == data.msg_total:
        #    print('closing connection', data.connid)
        #    sel.unregister(sock)
        #    sock.close()
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
