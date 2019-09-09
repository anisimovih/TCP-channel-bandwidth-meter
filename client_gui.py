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
        client_window.resize(802, 591)
        self.centralwidget = QtWidgets.QWidget(client_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.size_label.setObjectName("size_label")
        self.gridLayout.addWidget(self.size_label, 3, 3, 1, 1)
        self.entered_timelimit = QtWidgets.QLincleEdit(self.centralwidget)
        self.entered_timelimit.setObjectName("entered_timelimit")
        self.gridLayout.addWidget(self.entered_timelimit, 4, 4, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6);")
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 5, 0, 1, 2)
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 3, 1, 1, 1)
        self.entered_size = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_size.setObjectName("entered_size")
        self.gridLayout.addWidget(self.entered_size, 4, 3, 1, 1)
        self.entered_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_filename.setObjectName("entered_filename")
        self.gridLayout.addWidget(self.entered_filename, 4, 2, 1, 1)
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        self.filename_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.filename_label.setObjectName("filename_label")
        self.gridLayout.addWidget(self.filename_label, 3, 2, 1, 1)
        self.entered_port = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_port.setObjectName("entered_port")
        self.gridLayout.addWidget(self.entered_port, 4, 1, 1, 1)
        self.entered_ip = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_ip.setObjectName("entered_ip")
        self.gridLayout.addWidget(self.entered_ip, 4, 0, 1, 1)
        self.ip_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_label.setMaximumSize(QtCore.QSize(1677721, 15))
        self.ip_label.setObjectName("ip_label")
        self.gridLayout.addWidget(self.ip_label, 3, 0, 1, 1)
        self.checkBox_timelimit = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_timelimit.setObjectName("checkBox_timelimit")
        self.gridLayout.addWidget(self.checkBox_timelimit, 3, 4, 1, 1)
        self.change_to_server_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_to_server_button.setMaximumSize(QtCore.QSize(400, 16777215))
        self.change_to_server_button.setObjectName("change_to_server_button")
        self.gridLayout.addWidget(self.change_to_server_button, 5, 3, 1, 2)
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setMaximumSize(QtCore.QSize(16777215, 80))
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 2, 0, 1, 5)
        self.graph_field = QtWidgets.QWidget(self.centralwidget)
        self.graph_field.setObjectName("graph_field")
        self.gridLayout.addWidget(self.graph_field, 1, 0, 1, 5)
        self.horizontalLayout.addLayout(self.gridLayout)
        client_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(client_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        client_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(client_window)
        self.statusbar.setObjectName("statusbar")
        client_window.setStatusBar(self.statusbar)

        self.retranslateUi(client_window)
        QtCore.QMetaObject.connectSlotsByName(client_window)

    def retranslateUi(self, client_window):
        _translate = QtCore.QCoreApplication.translate
        client_window.setWindowTitle(_translate("client_window", "SpeedTest(client)"))
        self.size_label.setText(_translate("client_window", "Size:"))
        self.start_button.setText(_translate("client_window", "Start"))
        self.port_label.setText(_translate("client_window", "Port:"))
        self.filename_label.setText(_translate("client_window", "Filename:"))
        self.ip_label.setText(_translate("client_window", "IP:"))
        self.checkBox_timelimit.setText(_translate("client_window", "Time limit(seconds):"))
        self.change_to_server_button.setText(_translate("client_window", "Change to server"))
