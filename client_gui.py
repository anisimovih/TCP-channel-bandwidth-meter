# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_for_client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_client_window(object):
    def setupUi(self, client_window):
        client_window.setObjectName("client_window")
        client_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(client_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.entered_port = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_port.setObjectName("entered_port")
        self.gridLayout.addWidget(self.entered_port, 3, 1, 1, 1)
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        self.filename_label.setObjectName("filename_label")
        self.gridLayout.addWidget(self.filename_label, 2, 2, 1, 1)
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.setObjectName("size_label")
        self.gridLayout.addWidget(self.size_label, 2, 3, 1, 1)
        self.entered_size = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_size.setObjectName("entered_size")
        self.gridLayout.addWidget(self.entered_size, 3, 3, 1, 1)
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 2, 1, 1, 1)
        self.entered_ip = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_ip.setObjectName("entered_ip")
        self.gridLayout.addWidget(self.entered_ip, 3, 0, 1, 1)
        self.entered_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_filename.setObjectName("entered_filename")
        self.gridLayout.addWidget(self.entered_filename, 3, 2, 1, 1)
        self.ip_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_label.setMaximumSize(QtCore.QSize(1677721, 20))
        self.ip_label.setObjectName("ip_label")
        self.gridLayout.addWidget(self.ip_label, 2, 0, 1, 1)
        self.graph_field = QtWidgets.QWidget(self.centralwidget)
        self.graph_field.setObjectName("graph_field")
        self.gridLayout.addWidget(self.graph_field, 0, 0, 1, 4)
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setMaximumSize(QtCore.QSize(16777215, 80))
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 1, 0, 1, 4)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6);")
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 4, 0, 1, 2)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setStyleSheet("background-color: rgb(204, 0, 0);")
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 4, 2, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        client_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(client_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        client_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(client_window)
        self.statusbar.setObjectName("statusbar")
        client_window.setStatusBar(self.statusbar)

        self.retranslateUi(client_window)
        QtCore.QMetaObject.connectSlotsByName(client_window)

    def retranslateUi(self, client_window):
        _translate = QtCore.QCoreApplication.translate
        client_window.setWindowTitle(_translate("client_window", "SpeedTest"))
        self.filename_label.setText(_translate("client_window", "Filename:"))
        self.size_label.setText(_translate("client_window", "Size:"))
        self.port_label.setText(_translate("client_window", "Port:"))
        self.ip_label.setText(_translate("client_window", "IP:"))
        self.start_button.setText(_translate("client_window", "Start"))
        self.stop_button.setText(_translate("client_window", "Stop"))
