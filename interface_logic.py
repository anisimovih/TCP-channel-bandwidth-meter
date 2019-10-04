# TODO: перенести взаимодействие с графиком в его класс
import sys  # sys нужен для передачи argv в QApplication

from graph import Graph


from PyQt5 import QtCore, QtWidgets
# from PyQt5.Qt import (QMessageBox)

import threads
import client
import global_variables
from catching_fall_errors import log_uncaught_exceptions
import client_gui
import server_gui
import choise_gui


sys.excepthook = log_uncaught_exceptions  # Ловим ошибку в слотах, если приложение просто падает без стека


class WorkingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.trans = QtCore.QTranslator(self)
        # self.console.triggered.connect(self.change_language)
        self.thread = None
        self.graph = None

    @QtCore.pyqtSlot(str)
    def change_language(self, language):
        # TODO: Добавить языки для сервера
        if language == "eng":
            self.trans.load('ru-eng')
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        """Переопределение метода для переключения языков."""
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
        super(WorkingWindow, self).changeEvent(event)

    '''explanation to @QtCore.pyqtSlot:
       provide a C++ signature for method, thereby reduce the amount of memory used and is slightly faster'''

    @QtCore.pyqtSlot()
    def on_start_button_click(self):
        self.save_user_prefs()
        if global_variables.what_to_join == 's':
            global_variables.ip = self.entered_ip.text()

            if self.checkBox_packetLimit.isChecked():
                global_variables.packet_limit = int(self.entered_packetLimit.text())

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

    def stop_thread(self):
        global_variables.thread_1_active = False
        self.thread = None
        '''self.thread_2.terminate()
        self.thread_2 = None'''
        self.start_button.setStyleSheet("background-color: rgb(78, 154, 6)")
        self.start_button.setText("Start")
        self.console.append(global_variables.termination_reason)

    @staticmethod
    def stop():
        global_variables.thread_1_active = False
        # Если это сервер, то делаем пустой коннект, чтобы выйти из ожидания.
        # TODO: удалить global_variables.graph_y (graph_y = [0]  # Координата Y графика)
        #  больше не существует, остановка не работает
        #if global_variables.what_to_join == 'c' and len(global_variables.graph_y) == 1:
        if global_variables.what_to_join == 'c':
            with open("user_prefs.txt", "r") as user_prefs:
                text = user_prefs.read().splitlines()
                client.connect_to_server("127.0.0.1", int(text[1]), int(text[2]), text[3])

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


class ClientWindow(WorkingWindow, client_gui.Ui_client_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMouseTracking(True)
        self.start_button.clicked.connect(lambda: self.on_start_button_click())
        with open("user_prefs.txt", "r") as user_prefs:
            text = user_prefs.read().splitlines()
            self.entered_ip.setText(text[0])
            self.entered_port.setText(text[1])
            self.entered_size.setText(text[2])
            self.entered_filename.setText(text[3])

        self.actionEndglish.triggered.connect(lambda: self.change_language('eng'))
        self.action_5.triggered.connect(lambda: self.change_language('ru'))


class ServerWindow(WorkingWindow, server_gui.Ui_server_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start_button.clicked.connect(lambda: self.on_start_button_click())
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
