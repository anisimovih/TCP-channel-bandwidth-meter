import global_variables

from client import connect_to_server
from PyQt5.QtCore import (QThread, pyqtSignal)


# Подклассификация QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    threadSignalAThread = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        # Аргументы pyqtSignal определяют типы объектов, которые будут emit (испускаться) на этом сигнале
        self.threadSignalAThread.emit(1)  # значение в скобках пока не выяснил
        global_variables.graph_active = True
        connect_to_server(global_variables.ip,
                          global_variables.port,
                          global_variables.size,
                          global_variables.filename)
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
