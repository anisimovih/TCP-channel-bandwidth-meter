# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_server_window(object):
    def setupUi(self, server_window):
        server_window.setObjectName("server_window")
        server_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(server_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setMaximumSize(QtCore.QSize(16777215, 80))
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 2, 0, 1, 4)
        self.entered_size = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_size.setObjectName("entered_size")
        self.gridLayout.addWidget(self.entered_size, 4, 3, 1, 1)
        self.entered_port = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_port.setObjectName("entered_port")
        self.gridLayout.addWidget(self.entered_port, 4, 1, 1, 1)
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        self.filename_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.filename_label.setObjectName("filename_label")
        self.gridLayout.addWidget(self.filename_label, 3, 2, 1, 1)
        self.entered_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_filename.setObjectName("entered_filename")
        self.gridLayout.addWidget(self.entered_filename, 4, 2, 1, 1)
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.size_label.setObjectName("size_label")
        self.gridLayout.addWidget(self.size_label, 3, 3, 1, 1)
        self.graph_field = QtWidgets.QWidget(self.centralwidget)
        self.graph_field.setObjectName("graph_field")
        self.gridLayout.addWidget(self.graph_field, 1, 0, 1, 4)
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 3, 1, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6);")
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 5, 0, 1, 2)
        self.change_to_client_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_to_client_button.setMaximumSize(QtCore.QSize(400, 16777215))
        self.change_to_client_button.setObjectName("change_to_client_button")
        self.gridLayout.addWidget(self.change_to_client_button, 5, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        server_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(server_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        server_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(server_window)
        self.statusbar.setObjectName("statusbar")
        server_window.setStatusBar(self.statusbar)

        self.retranslateUi(server_window)
        QtCore.QMetaObject.connectSlotsByName(server_window)

    def retranslateUi(self, server_window):
        _translate = QtCore.QCoreApplication.translate
        server_window.setWindowTitle(_translate("server_window", "Имитатор TCP соединения (сервер)"))
        self.filename_label.setText(_translate("server_window", "Имя файла:"))
        self.size_label.setText(_translate("server_window", "Размер сообщения:"))
        self.port_label.setText(_translate("server_window", "Порт:"))
        self.start_button.setText(_translate("server_window", "Старт"))
        self.change_to_client_button.setText(_translate("server_window", "Переход к окну \"Клиент\""))
