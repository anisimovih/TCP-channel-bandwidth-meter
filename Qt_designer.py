# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_for_client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from graph import MyDynamicMplCanvas
import global_variables


class UiMainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.entered_port = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_port.setObjectName("entered_port")
        self.gridLayout.addWidget(self.entered_port, 3, 1, 1, 1)
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setObjectName("label_filename")
        self.gridLayout.addWidget(self.label_filename, 2, 2, 1, 1)
        self.label_size = QtWidgets.QLabel(self.centralwidget)
        self.label_size.setObjectName("label_size")
        self.gridLayout.addWidget(self.label_size, 2, 3, 1, 1)
        self.entered_size = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_size.setObjectName("entered_size")
        self.gridLayout.addWidget(self.entered_size, 3, 3, 1, 1)
        self.label_port = QtWidgets.QLabel(self.centralwidget)
        self.label_port.setObjectName("label_port")
        self.gridLayout.addWidget(self.label_port, 2, 1, 1, 1)
        self.entered_IP = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_IP.setObjectName("entered_IP")
        self.gridLayout.addWidget(self.entered_IP, 3, 0, 1, 1)
        self.entered_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_filename.setObjectName("entered_filename")
        self.gridLayout.addWidget(self.entered_filename, 3, 2, 1, 1)
        self.label_IP = QtWidgets.QLabel(self.centralwidget)
        self.label_IP.setMaximumSize(QtCore.QSize(1677721, 20))
        self.label_IP.setObjectName("label_IP")
        self.gridLayout.addWidget(self.label_IP, 2, 0, 1, 1)
        '''graph'''
        self.widget = QtWidgets.QWidget(self.centralwidget)
        dc = MyDynamicMplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(dc, 0, 0, 1, 4)
        ''' '''
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setMaximumSize(QtCore.QSize(16777215, 80))
        self.console.setObjectName("console")
        #self.console.setText(str(global_variables.console))
        #global_variables.console += 1
        self.gridLayout.addWidget(self.console, 1, 0, 1, 4)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6);")
        self.start_button.setObjectName("start_button")

        self.start_button.clicked.connect(self.on_start_button_click)

        self.gridLayout.addWidget(self.start_button, 4, 0, 1, 2)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setStyleSheet("background-color: rgb(204, 0, 0);")
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 4, 2, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SpeedTest"))
        self.label_filename.setText(_translate("MainWindow", "Filename:"))
        self.label_size.setText(_translate("MainWindow", "Size:"))
        self.label_port.setText(_translate("MainWindow", "Port:"))
        self.label_IP.setText(_translate("MainWindow", "IP:"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
