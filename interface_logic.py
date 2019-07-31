import sys
import global_variables
import csv
import os.path

from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import (QMessageBox)

from client import connect_to_server
from Qt_designer import UiMainWindow
from catching_fall_errors import log_uncaught_exceptions
from threads import AThread

ip = 0
sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.start_button.clicked.connect(self.using_a_thread)

        self.thread_2 = None
        self.thread = None
        self.objThread = None

        self.stop_button.clicked.connect(self.on_stop_button_click)
        self.entered_IP.setText("127.0.0.1")
        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("client.csv")

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.printing_to_console)
        timer.start(1000)

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

    '''ИСПРАВИТЬ: выводит результаты только после окончания передачи'''
    def printing_to_console(self):
        if os.path.exists("client.csv"):
            with open("client.csv", "r") as f_obj:
                reader = csv.DictReader(f_obj, delimiter=';')
                for line in reader:
                    self.console.append("Пакет №" + line["number"] + " отправлен со средней скоростью " + str(
                        round(float(line["speed"]))) + " Б/с")

    # ---- AThread(QThread) -----------#
    def using_a_thread(self):
        if self.thread is None:
            self.thread = AThread()
            # self.thread_2 = BThread()
            # self.thread.finished.connect(self.finished_a_thread)  # если поток может закончить выполнение
            self.thread.start()
            global_variables.thread_1 = True
            # self.thread_2.start()
            self.start_button.setText("Stop AThread(QThread)")

        else:
            if global_variables.thread_1:
                self.thread.terminate()
            self.thread = None
            '''self.thread_2.terminate()
            self.thread_2 = None'''
            self.start_button.setText("Start AThread(QThread)")

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

            '''if self.thread_2:
                self.thread_2.quit()
            del self.thread_2'''

            super(MainWindow, self).closeEvent(event)  # работает и без этого
        else:
            event.ignore()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
exit(app.exec_())
