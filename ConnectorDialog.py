# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HandlerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Connector_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Connect to server")
        Dialog.resize(250, 133)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 231, 121))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 199, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ip_address_label = QtWidgets.QLabel(self.layoutWidget)
        self.ip_address_label.setObjectName("ip_address_label")
        self.verticalLayout_2.addWidget(self.ip_address_label)
        self.port_label = QtWidgets.QLabel(self.layoutWidget)
        self.port_label.setObjectName("port_label")
        self.verticalLayout_2.addWidget(self.port_label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        #--------------------------------------------------------------------------------
        #ask user for ip address
        self.ip_address_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.ip_address_lineEdit.setObjectName("ip_address_lineEdit")
        self.verticalLayout.addWidget(self.ip_address_lineEdit)
        #--------------------------------------------------------------------------------
        #ask user for port number
        self.port_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.port_lineEdit.setObjectName("port_lineEdit")
        self.verticalLayout.addWidget(self.port_lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        
        
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)  
        
        
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def start_server(self):
        self.tcp_server = QTcpServer()
        self.tcp_server.listen(QHostAddress(SERVER_ADDRESS), SERVER_PORT)
        self.tcp_server.newConnection.connect(self.connect_client)
        self.clients = []

        try:
            address = ""
            address, ok = self.ip_address_lineEdit.getText(self, "ip_address_lineEdit")
            if ok:
                if address.strip():

                    ServerProcess.ipFormatChk(self, address)
                else:
                    self.events_textEdit.setText("Input line is empty, enter IP-address")
            else:
                self.events_textEdit.setText("You have an glitch")

        except socket.error:
           time.sleep(3.0)
           self.events_textEdit.setText("[+] ip and port is closed")
           self.events_textEdit.append('Socket connect failed! Loop up and try socket again') 

    def ipFormatChk(self, address): 

        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, address):
            address = QHostAddress(address)
            self.port_lineEdit.setText("[+] Your ip adress was valid")
            PORT = ""
            PORT, ok = QInputDialog.getText(self, "Handler", "Enter PORT: ")
            PORT = int(PORT)
            if ok:
                self.events_textEdit.append("[+] Your port was also valid")
                #recmGui.App.connect_client(self, address, PORT)
                #if not ServerProcess tcpServer.listen(address, PORT) which means if not ok then print can't listen, if ok then listen
                self.events_textEdit.append("[+] The server is listening on the ip address and port, waiting for connections")

                Server.ServerProcess.tcpServer.newConnection.connect(Server.ServerProcess.connect_client(address, PORT))
                
                if not Server.ServerProcess.tcpServer.listen(address, PORT):
                    self.events_textEdit.append("[+] address and port are not available")
                    self.close()
                    #tomorrow you will have to reasses if this llisten statement should be in a loops
                    return
                    
                #ServerProcess.tcpServer.waitForNewConnection(ServerProcess.connect_client(self))
                #ServerProcess.connect_client()
                    #self.squareTab1.setText("[+] We made it this far. return true please")
                    #print("recmServerThread thread: {}".format(self.thread()))
                    #self.squareTab1.setText("[+] client just connected to the socket what is your orders master")
                    #print("recmServerThread thread: {}".format(self.thread()))
      
        else:
            self.events_textEdit.setText("You have a ip address or port issue, try again")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Connect to server"))
        self.groupBox.setTitle(_translate("Dialog", "Connection Setup"))


        self.ip_address_label.setText(_translate("Dialog", "IP Address"))


        self.port_label.setText(_translate("Dialog", "Port"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Handler_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
