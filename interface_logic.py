# TODO: поменять бесконечные циклы на зависимые от перемнных через поток
import sys  # sys нужен для передачи argv в QApplication

from graph import MyDynamicMplCanvas
from catching_fall_errors import log_uncaught_exceptions

import threads
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import (QMessageBox)

import client_gui
import server_gui
import choise_gui
import client
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

        self.graph = None


        '''timer = QtCore.QTimer(self)
        timer.timeout.connect(self.printing_to_console)
        timer.start(500)'''

    '''explanation to @QtCore.pyqtSlot:
       provide a C++ signature for method, thereby reduce the amount of memory used and is slightly faster'''
    @QtCore.pyqtSlot()
    def on_start_button_click(self, need_of_ip):
        self.save_user_prefs()
        if need_of_ip:
            global_variables.ip = self.entered_ip.text()
        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()
        self.using_a_thread()

    def save_user_prefs(self):
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
        with open("user_prefs.txt", "w") as user_prefs:
            if global_variables.what_to_join == 's':
                user_prefs.writelines([self.entered_ip.text().rstrip() + '\n',
                                       self.entered_port.text().rstrip() + '\n',
                                       self.entered_size.text().rstrip() + '\n',
                                       self.entered_filename.text().rstrip() + '\n',
                                       text[4] + '\n'])
            else:
                user_prefs.writelines([text[0] + '\n',
                                       self.entered_port.text().rstrip() + '\n',
                                       self.entered_size.text().rstrip() + '\n',
                                       text[3] + '\n',
                                       self.entered_filename.text().rstrip()])
    """@QtCore.pyqtSlot()
    def on_stop_button_click(self):
        # self.close()
        self.switch_on_server()"""

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
            self.thread = threads.AThread()
            self.thread.finished.connect(lambda: self.stop_thread())
            #global_variables.clint_active = True
            self.thread.start()
            # self.thread_2 = BThread()
            # self.thread.finished.connect(self.finished_a_thread)  # если поток может закончить выполнение
            global_variables.thread_1_active = True
            # self.thread_2.start()
            self.start_button.setStyleSheet("background-color: rgb(204, 0, 0)")
            self.start_button.setText("Stop")
        else:
            self.stop_server()

    def stop_thread(self):
        global_variables.thread_1_active = False
        self.thread = None
        '''self.thread_2.terminate()
        self.thread_2 = None'''
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6)")
        self.start_button.setText("Start")
        self.console.append(global_variables.termination_reason)

    @staticmethod
    def stop_server():
        global_variables.thread_1_active = False
        # Если это сервер, то делаем пустой коннект, чтобы выйти из ожидания.
        if global_variables.what_to_join == 'c':
            with open("user_prefs.txt", "r") as user_prefs:
                text = user_prefs.read().splitlines()
                client.connect_to_server("127.0.0.1", int(text[1]), int(text[2]), text[3])

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

    def add_graph(self):
        self.graph = MyDynamicMplCanvas(self.graph_field, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.graph, 1, 0, 1, 4)


class ClientWindow(WorkingWindow, client_gui.Ui_client_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start_button.clicked.connect(lambda: self.on_start_button_click(True))
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
            self.entered_ip.setText(text[0])
            self.entered_port.setText(text[1])
            self.entered_size.setText(text[2])
            self.entered_filename.setText(text[3])


class ServerWindow(WorkingWindow, server_gui.Ui_server_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start_button.clicked.connect(lambda: self.on_start_button_click(False))
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
            self.entered_port.setText(text[1])
            self.entered_size.setText(text[2])
            self.entered_filename.setText(text[4])


class CrossWindow(QtWidgets.QMainWindow, choise_gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client_window = ClientWindow()
        self.server_window = ServerWindow()
        self.client_button.clicked.connect(lambda: self.show_window(self.client_window, 's'))
        self.server_button.clicked.connect(lambda: self.show_window(self.server_window, 'c'))

    def show_window(self, window_name, window_abr):
        self.close()
        window_name.add_graph()
        global_variables.what_to_join = window_abr
        self.buttons_connect()
        window_name.show()

    def buttons_connect(self):
        self.client_window.change_to_server_button.clicked.connect(lambda: self.change_window(self.client_window, self.server_window, 'c'))
        self.server_window.change_to_client_button.clicked.connect(lambda: self.change_window(self.server_window, self.client_window, 's'))

    @staticmethod
    def change_window(from_window, to_window, window_abr):
        to_window.add_graph()
        if global_variables.thread_1_active:
            from_window.stop_thread()
        from_window.graph.deleteLater()
        global_variables.what_to_join = window_abr
        '''from_window.stop_thread()
        if global_variables.thread_1_active and window_abr == 'c':
            to_window.stop_thread()'''
        from_window.close()
        to_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CrossWindow()
    window.show()
    app.exec_()
