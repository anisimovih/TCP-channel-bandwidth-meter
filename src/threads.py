from PyQt5.QtCore import (QThread, pyqtSignal)

from src import global_variables
from src.client import connect_to_server
from src.server import connect_to_client
from src.graph import Graph


# Подклассификация QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    threadSignalAThread = pyqtSignal(int)

    def __init__(self, graph):
        super().__init__()
        self.graph = graph

    def run(self):
        # Аргументы pyqtSignal определяют типы объектов, которые будут emit (испускаться) на этом сигнале
        self.threadSignalAThread.emit(1)  # значение в скобках пока не выяснил
        print(global_variables.ip,
              int(global_variables.port),
              int(global_variables.size),
              global_variables.filename)
        if global_variables.what_to_join == "s":
            connect_to_server(global_variables.ip,
                              int(global_variables.port),
                              int(global_variables.size),
                              global_variables.filename)
            #interface_logic.WorkingWindow.stop_thread(interface_logic.CrossWindow.client_window)
        else:
            connect_to_client(int(global_variables.port),
                              int(global_variables.size),
                              global_variables.filename,
                              self.graph)
            #print("End!")

        '''count = 1
        while True:
            global_variables.graph_y.append(count)
            count += 1
            AThread.sleep(1)'''


'''class BThread(QThread):
    threadSignalBThread = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        self.threadSignalBThread.emit(1)
        while True:
            print("thread_2\n")
            BThread.sleep(1)'''
