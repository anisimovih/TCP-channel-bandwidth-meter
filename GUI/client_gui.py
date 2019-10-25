# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_gui.ui'
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
        self.entered_packetLimit = QtWidgets.QLineEdit(self.centralwidget)
        self.entered_packetLimit.setObjectName("entered_packetLimit")
        self.gridLayout.addWidget(self.entered_packetLimit, 4, 4, 1, 1)
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
        self.checkBox_packetLimit = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_packetLimit.setObjectName("checkBox_packetLimit")
        self.gridLayout.addWidget(self.checkBox_packetLimit, 3, 4, 1, 1)
        self.console = QtWidgets.QTextEdit(self.centralwidget)
        self.console.setMaximumSize(QtCore.QSize(16777215, 80))
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 2, 0, 1, 5)
        self.graph_field = QtWidgets.QWidget(self.centralwidget)
        self.graph_field.setObjectName("graph_field")
        self.gridLayout.addWidget(self.graph_field, 1, 0, 1, 5)
        self.change_to_server_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_to_server_button.setMaximumSize(QtCore.QSize(400, 16777215))
        self.change_to_server_button.setObjectName("change_to_server_button")
        self.gridLayout.addWidget(self.change_to_server_button, 5, 4, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        client_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(client_window)
        self.statusbar.setObjectName("statusbar")
        client_window.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(client_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_language = QtWidgets.QMenu(self.menu)
        self.menu_language.setObjectName("menu_language")
        self.menu_connection_type = QtWidgets.QMenu(self.menu)
        self.menu_connection_type.setObjectName("menu_connection_type")
        self.menu_UDP = QtWidgets.QMenu(self.menu_connection_type)
        self.menu_UDP.setObjectName("menu_UDP")
        client_window.setMenuBar(self.menubar)
        self.action_russian = QtWidgets.QAction(client_window)
        self.action_russian.setEnabled(False)
        self.action_russian.setObjectName("action_russian")
        self.action_english = QtWidgets.QAction(client_window)
        self.action_english.setObjectName("action_english")
        self.action_remove_graph = QtWidgets.QAction(client_window)
        self.action_remove_graph.setObjectName("action_remove_graph")
        self.action_TCP = QtWidgets.QAction(client_window)
        self.action_TCP.setEnabled(False)
        self.action_TCP.setObjectName("action_TCP")
        self.actionss = QtWidgets.QAction(client_window)
        self.actionss.setObjectName("actionss")
        self.menu_language.addSeparator()
        self.menu_language.addAction(self.action_russian)
        self.menu_language.addSeparator()
        self.menu_language.addAction(self.action_english)
        self.menu_connection_type.addAction(self.action_TCP)
        self.menu_connection_type.addSeparator()
        self.menu_connection_type.addAction(self.menu_UDP.menuAction())
        self.menu.addAction(self.menu_language.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.menu_connection_type.menuAction())
        self.menu.addAction(self.action_remove_graph)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(client_window)
        QtCore.QMetaObject.connectSlotsByName(client_window)

    def retranslateUi(self, client_window):
        _translate = QtCore.QCoreApplication.translate
        client_window.setWindowTitle(_translate("client_window", "Имитатор TCP соединения (клиент)"))
        self.size_label.setText(_translate("client_window", "Размер сообщения:"))
        self.start_button.setText(_translate("client_window", "Старт"))
        self.port_label.setText(_translate("client_window", "Порт:"))
        self.filename_label.setText(_translate("client_window", "Имя файла:"))
        self.ip_label.setText(_translate("client_window", "IP:"))
        self.checkBox_packetLimit.setText(_translate("client_window", "Ограничение (число сообщений):"))
        self.change_to_server_button.setText(_translate("client_window", "Переход к окну \"Сервер\""))
        self.menu.setTitle(_translate("client_window", "Опции"))
        self.menu_language.setTitle(_translate("client_window", "Язык"))
        self.menu_connection_type.setTitle(_translate("client_window", "Тип соединения"))
        self.menu_UDP.setTitle(_translate("client_window", "UDP (задайте скорость)"))
        self.action_russian.setText(_translate("client_window", "Русский"))
        self.action_english.setText(_translate("client_window", "English"))
        self.action_remove_graph.setText(_translate("client_window", "Очистить график"))
        self.action_TCP.setText(_translate("client_window", "TCP"))
        self.actionss.setText(_translate("client_window", "ss"))
