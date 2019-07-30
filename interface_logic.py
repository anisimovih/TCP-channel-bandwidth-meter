# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_for_client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


# from __future__ import unicode_literals
import sys
import axes

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5 import Qt

from Client import connect
from Qt_designer import UiMainWindow
from catching_fall_errors import log_uncaught_exceptions

sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


# Подклассификация QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    threadSignalAThread = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        count = 0
        while count < 1000:
            # time.sleep(1)
            Qt.QThread.msleep(2000)
            count += 1
            self.threadSignalAThread.emit(count)
            axes.graph_y.append(count)


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.start_button.clicked.connect(self.using_q_thread)

        self.thread = None
        self.objThread = None

        self.stop_button.clicked.connect(self.on_stop_button_click)
        self.entered_IP.setText("127.0.0.1")
        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("client.csv")

    @QtCore.pyqtSlot()
    def on_start_button_click(self):
        ip = self.entered_IP.text()
        port = self.entered_port.text()
        filename = self.entered_filename.text()
        size = self.entered_size.text()
        connect(ip, port, size, filename)

    @QtCore.pyqtSlot()
    def on_stop_button_click(self):
        self.close()

    # ---- AThread(QThread) -----------#
    def using_q_thread(self):
        if self.thread is None:
            self.thread = AThread()
            self.thread.finished.connect(self.finishedAThread)
            self.thread.start()
            self.start_button.setText("Stop AThread(QThread)")
        else:
            self.thread.terminate()
            self.thread = None
            self.start_button.setText("Start AThread(QThread)")

    def finishedAThread(self):
        self.thread = None
        self.start_button.setText("Start AThread(QThread)")

    # --END-- AThread(QThread) -------------------#

    def closeEvent(self, event):
        reply = Qt.QMessageBox.question \
            (self, 'Информация',
             "Вы уверены, что хотите закрыть приложение?",
             Qt.QMessageBox.Yes,
             Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.Yes:
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
