import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import csv
import os.path
import client_gui  # Это наш конвертированный файл дизайна
import global_variables
import PyQt5

from graph import MyDynamicMplCanvas
from catching_fall_errors import log_uncaught_exceptions
from threads import AThread
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import (QMessageBox)

sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


class ExampleApp(QtWidgets.QMainWindow, client_gui.Ui_client_window):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        ''''добавляем график'''
        dc = MyDynamicMplCanvas(self.centralwidget, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(dc, 0, 0, 1, 4)

        self.start_button.clicked.connect(self.on_start_button_click)

        self.thread_2 = None
        self.thread = None
        self.objThread = None

        self.thread_2 = None
        self.thread = None
        self.objThread = None

        self.stop_button.clicked.connect(self.on_stop_button_click)
        self.entered_ip.setText("127.0.0.1")
        self.entered_port.setText("10002")
        self.entered_size.setText("1000")
        self.entered_filename.setText("client.csv")

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.printing_to_console)
        timer.start(1000)

    @QtCore.pyqtSlot()
    def on_start_button_click(self):
        global_variables.ip = self.entered_ip.text()
        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()
        self.using_a_thread()

    @QtCore.pyqtSlot()
    def on_stop_button_click(self):
        # self.close()
        global_variables.ip = self.entered_ip.text()
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

            super(ExampleApp, self).closeEvent(event)  # работает и без этого
        else:
            event.ignore()


def main():
        app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        window = ExampleApp()  # Создаём объект класса ExampleApp
        window.show()  # Показываем окно
        app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
