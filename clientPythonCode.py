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
            ui.address = Connector_ui.ip_address_lineEdit.text()
            ui.port = Connector_ui.port_lineEdit.text()
              
        else:
            ui.console_textEdit.append("you have quit the connector dialog")







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
