# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_for_client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


# from __future__ import unicode_literals
import sys
import global_variables

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5.Qt import (QMessageBox)

from Client import connect_to_server
from Qt_designer import UiMainWindow
from catching_fall_errors import log_uncaught_exceptions

ip = 0
sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


# Подклассификация QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    threadSignalAThread = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        self.threadSignalAThread.emit(1)
        count = 1
        global_variables.graph_active = True
        #connect_to_server(global_variables.ip,
        #                  global_variables.port,
         #                 global_variables.size,
         #                 global_variables.filename)
        while True:
            global_variables.graph_y.append(count)
            count += 1
            QThread.sleep(1)


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.start_button.clicked.connect(self.using_a_thread)

        self.thread = None
        self.objThread = None

        self.stop_button.clicked.connect(self.on_stop_button_click)
        self.entered_IP.setText("127.0.0.1")
        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("client.csv")

    @QtCore.pyqtSlot()
    def on_start_button_click(self):
        global_variables.ip = self.entered_IP.text()
        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()

    @QtCore.pyqtSlot()
    def on_stop_button_click(self):
        # self.close()
        global_variables.ip = self.entered_IP.text()
        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()

    # ---- AThread(QThread) -----------#
    def using_a_thread(self):
        if self.thread is None:
            self.thread = AThread()
            self.thread.finished.connect(self.finished_a_thread)  # смысл не установлен
            self.thread.start()
            self.start_button.setText("Stop AThread(QThread)")
        else:
            self.thread.terminate()
            self.thread = None
            self.start_button.setText("Start AThread(QThread)")

    def finished_a_thread(self):
        self.thread = None
        self.start_button.setText("Start AThread(QThread)")

    # --END-- AThread(QThread) -------------------#

    def closeEvent(self, event):
        reply = QMessageBox.question \
            (self, 'Информация',
             "Вы уверены, что хотите закрыть приложение?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.thread:
                self.thread.quit()
            del self.thread

            super(MainWindow, self).closeEvent(event)  # смысл не установлен
        else:
            event.ignore()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
exit(app.exec_())
