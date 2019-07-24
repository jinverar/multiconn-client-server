# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConnectorDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Connector_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(319, 214)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ip_address_label = QtWidgets.QLabel(self.groupBox)
        self.ip_address_label.setObjectName("ip_address_label")
        self.verticalLayout.addWidget(self.ip_address_label)
        self.port_label = QtWidgets.QLabel(self.groupBox)
        self.port_label.setObjectName("port_label")
        self.verticalLayout.addWidget(self.port_label)
        self.num_conns_label = QtWidgets.QLabel(self.groupBox)
        self.num_conns_label.setObjectName("num_conns_label")
        self.verticalLayout.addWidget(self.num_conns_label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ip_address_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ip_address_lineEdit.setObjectName("ip_address_lineEdit")
        self.verticalLayout_2.addWidget(self.ip_address_lineEdit)
        self.port_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.port_lineEdit.setObjectName("port_lineEdit")
        self.verticalLayout_2.addWidget(self.port_lineEdit)
        self.num_conns_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.num_conns_lineEdit.setObjectName("num_conns_lineEdit")
        self.verticalLayout_2.addWidget(self.num_conns_lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Connect to server setup"))
        self.groupBox.setTitle(_translate("Dialog", "Connector Setup"))
        self.ip_address_label.setText(_translate("Dialog", "IP Address"))
        self.port_label.setText(_translate("Dialog", "Port"))
        self.num_conns_label.setText(_translate("Dialog", "Num_conns"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
