# TODO: перенести взаимодействие с графиком в его класс
# 10.0.74.152
import sys  # sys нужен для передачи argv в QApplication
import socket

from PyQt5 import QtCore, QtWidgets
# from PyQt5.Qt import (QMessageBox)

from src.graph import Graph
from src import threads, global_variables, client
from src.catching_fall_errors import log_uncaught_exceptions
from GUI import client_gui, choise_gui, server_gui

sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


class WorkingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.trans = QtCore.QTranslator(self)
        self.thread = None
        self.graph = None

    # <editor-fold desc="Actions">
    @QtCore.pyqtSlot(str)
    def change_language(self, language):
        # TODO: Добавить языки для сервера
        if language == "eng":
            self.trans.load('./translation/ru-eng')
            QtWidgets.QApplication.instance().installTranslator(self.trans)
            self.action_english.setEnabled(False)
            self.action_russian.setEnabled(True)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)
            self.action_english.setEnabled(True)
            self.action_russian.setEnabled(False)

    def changeEvent(self, event):
        """Переопределение метода для переключения языков."""
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
        super(WorkingWindow, self).changeEvent(event)

    def change_connection_type(self, new_connection_type):
        self.console.append("Тип соединения переключен на " + new_connection_type)
        if new_connection_type == 'TCP':
            global_variables.connection_type = 'TCP'
            self.action_TCP.setEnabled(False)
            if self.window == 'Server':
                self.action_UDP_.setEnabled(True)
        else:
            global_variables.connection_type = 'UDP'
            self.action_TCP.setEnabled(True)
            if self.window == 'Server':
                self.action_UDP_.setEnabled(False)
            else:
                global_variables.udp_speed = int(self.ql.text()) / 8
                print(global_variables.udp_speed)
                self.console.append("со скоростью " + self.ql.text() + " бит/сек.")


    '''explanation to @QtCore.pyqtSlot:
       provide a C++ signature for method, thereby reduce the amount of memory used and is slightly faster'''
    @QtCore.pyqtSlot()
    def on_start_button_click(self):
        self.save_user_prefs()
        if global_variables.what_to_join == 's':
            global_variables.ip = self.entered_ip.text()

            if self.checkBox_packetLimit.isChecked():
                global_variables.packet_limit = int(self.entered_packetLimit.text())
        else:
            if self.checkBox_speed_lim.isChecked():
                Graph.speed_limit = int(self.lineEdit_speed_lim.text())

        global_variables.port = self.entered_port.text()
        global_variables.filename = self.entered_filename.text()
        global_variables.size = self.entered_size.text()
        self.using_a_thread()

    # </editor-fold>

    def save_user_prefs(self):
        """
        Структура user_prefs:
        ip, port, size, client.csv path, server.csv path,
        активация отсечения аномалий, значение отсечения аномалий,
        активация ограничения пакетов, значение ограничения пакетов
        """
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
        with open("user_prefs.txt", "w") as user_prefs:
            if global_variables.what_to_join == 's':
                # Клиент:
                user_prefs.writelines([self.entered_ip.text().rstrip() + '\n',
                                       self.entered_port.text().rstrip() + '\n',
                                       self.entered_size.text().rstrip() + '\n',
                                       self.entered_filename.text().rstrip() + '\n',
                                       text[4] + '\n',
                                       text[5] + '\n',
                                       text[6] + '\n',
                                       "True\n" if self.checkBox_packetLimit.isChecked() else "False\n",
                                       self.entered_packetLimit.text().rstrip() + '\n',
                                       ])
            else:
                # Сервер:
                user_prefs.writelines([text[0] + '\n',
                                       self.entered_port.text().rstrip() + '\n',
                                       self.entered_size.text().rstrip() + '\n',
                                       text[3] + '\n',
                                       self.entered_filename.text().rstrip() + '\n',
                                       "True\n" if self.checkBox_speed_lim.isChecked() else "False\n",
                                       self.lineEdit_speed_lim.text().rstrip() + '\n',
                                       text[7] + '\n',
                                       text[8] + '\n'
                                       ])

    def printing_to_console(self, text):
        self.console.append(text)

    # <editor-fold desc="Threads">
    def using_a_thread(self):
        if self.thread is None:
            self.thread = threads.AThread(self.graph)
            self.thread.finished.connect(lambda: self.stop_thread())
            # global_variables.clint_active = True
            self.thread.start()
            # self.thread_2 = BThread()
            # self.thread.finished.connect(self.finished_a_thread)  # если поток может закончить выполнение
            global_variables.thread_1_active = True
            # self.thread_2.start()
            self.start_button.setStyleSheet("background-color: rgb(204, 0, 0)")
            self.start_button.setText("Stop")
        else:
            self.stop()

    def stop_thread(self, additional_reason=None):
        print("Поток передачи остановлен.")
        global_variables.thread_1_active = False
        self.thread = None
        '''self.thread_2.terminate()
        self.thread_2 = None'''
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6)")
        self.start_button.setText("Start")
        if additional_reason is not None:
            self.console.append(additional_reason)
        else:
            self.console.append(global_variables.termination_reason)
            global_variables.termination_reason = ''

    def stop(self):
        print("Остановка пользователем.")
        global_variables.thread_1_active = False
        # Если это сервер, то делаем пустой коннект, чтобы выйти из ожидания.
        if global_variables.what_to_join == 'c' and Graph.normal_speeds_quantity == 0:
            with open("user_prefs.txt", "r") as user_prefs:
                text = user_prefs.read().splitlines()
                client.connect_to_server("127.0.0.1", int(text[1]), int(text[2]), text[3])
        elif global_variables.what_to_join == 's':
            self.stop_thread("Фаервол не дает подключиться")
        elif global_variables.what_to_join == 'c' and global_variables.connection_type == 'UDP':
            with socket.socket(type=socket.SOCK_DGRAM) as sock:
                sock.sendto(b'end', ("127.0.0.1", int(global_variables.port)))

    # </editor-fold>

    '''def closeEvent(self, event):
        reply = QMessageBox.question \
            (self, 'Информация',
             "Вы уверены, что хотите закрыть приложение?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.thread:
                self.thread.quit()
            del self.thread
        else:
            event.ignore()'''

    # <editor-fold desc="Graph">
    def add_graph(self):
        self.graph = Graph(self.graph_field)
        self.graph.mpl_connect("button_press_event", self.on_press)
        self.graph.mpl_connect("button_release_event", self.on_release)
        self.graph.mpl_connect("motion_notify_event", self.on_move)
        self.graph.mpl_connect('scroll_event', self.on_scroll)
        self.gridLayout.addWidget(self.graph, 1, 0, 1, 5)

    def on_press(self, event):
        if event.button == 1:  # left
            Graph.select_start(self.graph, event)
        elif event.button == 3:
            Graph.pull_start(self.graph, event)

    def on_release(self, event):
        if event.button == 1:  # left
            Graph.select_stop(self.graph, event)
        elif event.button == 3:
            Graph.pull_stop(self.graph, event)

    def on_move(self, event):
        if event.button == 1:  # left
            Graph.select_update(self.graph, event)
        elif event.button == 3:
            Graph.pull_update(self.graph, event)

    def on_scroll(self, event):
        Graph.zoom(self.graph, event, self.graph.axes)

    # </editor-fold>


class ClientWindow(WorkingWindow, client_gui.Ui_client_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window = 'Client'
        self.ql = QtWidgets.QLineEdit("1200")
        self.setMouseTracking(True)
        self.start_button.clicked.connect(lambda: self.on_start_button_click())
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
            self.entered_ip.setText(text[0])
            self.entered_port.setText(text[1])
            self.entered_size.setText(text[2])
            self.entered_filename.setText(text[3])
            if text[7] == "True":
                self.checkBox_packetLimit.setChecked(True)
            self.entered_packetLimit.setText(text[8])

        self.action_english.triggered.connect(lambda: self.change_language('eng'))
        self.action_russian.triggered.connect(lambda: self.change_language('ru'))
        self.action_remove_graph.triggered.connect(lambda: Graph.clear_graph(self.graph))
        self.action_TCP.triggered.connect(lambda: self.change_connection_type('TCP'))

        self.menu_add_udp_limit()

    def menu_add_udp_limit(self):
        self.ql = QtWidgets.QLineEdit("1200")
        self.ql.setMinimumWidth(100)
        self.ql.textChanged.connect(self.on_udp_text_changed)
        self.ql.returnPressed.connect(lambda: self.change_connection_type('UDP'))  # нажатие на Enter
        udp_max_speed = QtWidgets.QWidgetAction(self)
        udp_max_speed.setDefaultWidget(self.ql)
        self.menu_UDP.addAction(udp_max_speed)

    @QtCore.pyqtSlot(str)
    def on_udp_text_changed(self, text):
        if text != "":
            try:
                global_variables.udp_speed = int(text) / 8
            except ValueError:
                self.ql.setText("1200")
                global_variables.udp_speed = 1200
                self.console.append("Введено неверное значение!")
        else:
            global_variables.udp_speed = 0


class ServerWindow(WorkingWindow, server_gui.Ui_server_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window = 'Server'
        self.start_button.clicked.connect(lambda: self.on_start_button_click())
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
            self.entered_port.setText(text[1])
            self.entered_size.setText(text[2])
            self.entered_filename.setText(text[4])
            if text[5] == "True":
                self.checkBox_speed_lim.setChecked(True)
            self.lineEdit_speed_lim.setText(text[6])
        self.connect_triggers()

    def connect_triggers(self):
        self.action_remove_graph.triggered.connect(lambda: Graph.clear_graph(self.graph))
        self.action_TCP.triggered.connect(lambda: self.change_connection_type('TCP'))
        self.action_UDP_.triggered.connect(lambda: self.change_connection_type('UDP'))
        self.action_lost_packets_off.triggered.connect(lambda: self.change_lost_packages_mapping(False))
        self.action_lost_packets_on.triggered.connect(lambda: self.change_lost_packages_mapping(True))

    def show_lost_packages(self):
        pass

    def change_lost_packages_mapping(self, trigger):
        if trigger:
            self.action_lost_packets_off.setEnabled(True)
            self.action_lost_packets_on.setEnabled(False)
            self.graph.points_trigger = True
            self.console.append("Включено отображение полученных пакетов.")
        else:
            self.action_lost_packets_off.setEnabled(False)
            self.action_lost_packets_on.setEnabled(True)
            self.graph.points_trigger = False
            self.console.append("Отображение полученных пакетов отключено.")
        Graph.draw_points(self.graph)
        self.graph.draw()


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
        self.client_window.change_to_server_button.clicked.connect(
            lambda: self.change_window(self.client_window, self.server_window, 'c'))
        self.server_window.change_to_client_button.clicked.connect(
            lambda: self.change_window(self.server_window, self.client_window, 's'))

    @staticmethod
    def change_window(from_window, to_window, window_abr):
        to_window.add_graph()
        if global_variables.thread_1_active:
            from_window.on_start_button_click()
        from_window.graph.deleteLater()
        global_variables.what_to_join = window_abr
        from_window.close()
        to_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CrossWindow()
    window.show()
    app.exec_()

    a = WorkingWindow()
