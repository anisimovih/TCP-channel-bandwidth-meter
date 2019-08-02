# TODO: поменять бесконечные циклы на зависимые от перемнных через поток
import sys  # sys нужен для передачи argv в QApplication
import csv
import os.path
import socket

from graph import MyDynamicMplCanvas
from catching_fall_errors import log_uncaught_exceptions
from threads import AThread
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import (QMessageBox)

import client_gui
import server_gui
import choise_gui
import global_variables

sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


class WorkingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.thread_2 = None
        self.thread = None
        self.objThread = None

        '''timer = QtCore.QTimer(self)
        timer.timeout.connect(self.printing_to_console)
        timer.start(500)'''

    '''explanation to @QtCore.pyqtSlot:
       provide a C++ signature for method, thereby reduce the amount of memory used and is slightly faster'''
    @QtCore.pyqtSlot()
    def on_start_button_click(self, need_of_ip):
        if need_of_ip:
            global_variables.ip = self.entered_ip.text()
        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()
        self.using_a_thread()

    @QtCore.pyqtSlot()
    def on_stop_button_click(self):
        # self.close()
        self.switch_on_server()

    '''ИСПРАВИТЬ: выводит результаты только после окончания передачи'''
    '''def printing_to_console(self):
        if os.path.exists("client.csv"):
            with open("client.csv", "r") as f_obj:
                reader = csv.DictReader(f_obj, delimiter=';')
                for line in reader:
                    self.console.append("Пакет №" + line["number"] + " отправлен со средней скоростью " + str(
                        round(float(line["speed"]))) + " Б/с")'''

    # ---- AThread(QThread) -----------#
    def using_a_thread(self):
        if self.thread is None:
            self.thread = AThread()
            self.thread.start()
            # self.thread_2 = BThread()
            # self.thread.finished.connect(self.finished_a_thread)  # если поток может закончить выполнение
            global_variables.thread_1_active = True
            # self.thread_2.start()
            self.start_button.setText("Stop AThread(QThread)")
        else:
            self.stop_thread()

    def stop_thread(self):
        if global_variables.thread_1_active:
            self.thread.terminate()
            #print("terminated")
            global_variables.thread_1_active = False
        self.thread = None
        '''self.thread_2.terminate()
        self.thread_2 = None'''
        self.start_button.setText("Start AThread(QThread)")
        # on_stop_thread

    def close_event(self, event):
        reply = QMessageBox.question \
            (self, 'Информация',
             "Вы уверены, что хотите закрыть приложение?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.thread:
                self.thread.quit()
            del self.thread

            '''if self.thread_2:
                self.thread_2.quit()
            del self.thread_2'''

            super(ClientWindow, self).close_event(event)  # работает и без этого
        else:
            event.ignore()


class ClientWindow(WorkingWindow, client_gui.Ui_client_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ''''добавляем график'''
        dc = MyDynamicMplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(dc, 1, 0, 1, 4)
        self.start_button.clicked.connect(lambda: self.on_start_button_click(True))

        self.entered_ip.setText("127.0.0.1")
        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("client.csv")


class ServerWindow(WorkingWindow, server_gui.Ui_server_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ''''добавляем график'''
        dc = MyDynamicMplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(dc, 1, 0, 1, 4)
        self.start_button.clicked.connect(lambda: self.on_start_button_click(False))

        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("server.csv")


class CrossWindow(QtWidgets.QMainWindow, choise_gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client_window = ClientWindow()
        self.server_window = ServerWindow()
        self.client_button.clicked.connect(lambda: self.show_client())
        self.server_button.clicked.connect(lambda: self.show_server())

    def show_client(self):
        self.close()
        self.client_window.change_to_server_button.clicked.connect(lambda: self.show_server())
        self.client_window.change_to_server_button.clicked.connect(self.client_window.close)
        global_variables.what_to_join = 's'
        self.client_window.stop_thread()
        self.client_window.show()

    def show_server(self):
        self.close()
        self.server_window.change_to_client_button.clicked.connect(lambda: self.show_client())
        self.server_window.change_to_client_button.clicked.connect(self.server_window.close)
        global_variables.what_to_join = 'c'
        self.client_window.stop_thread()
        self.server_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CrossWindow()
    window.show()
    app.exec_()
