from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import global_variables


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        self.activator()
        timer.timeout.connect(self.activator)
        timer.start(3000)

    def activator(self):
        if global_variables.graph_active:
            self.graph_active()
        else:
            self.graph_not_active()

    def graph_not_active(self):
        self.axes.cla()
        self.axes.plot([0], [0], 'ro')
        self.axes.set_xlabel("Номер пакета")
        self.axes.set_ylabel("Скорость (байт/сек)")
        self.draw()

    def graph_active(self):
        '''if len(global_variables.graph_y_only) > global_variables.graph_len:
            self.axes.plot(
                [
                    global_variables.graph_y_only[global_variables.graph_len - 1][0],
                    global_variables.graph_y_only[global_variables.graph_len][0]
                ],
                [
                    global_variables.graph_y_only[global_variables.graph_len - 1][1],
                    global_variables.graph_y_only[global_variables.graph_len][1]
                ],
                'r')

            global_variables.graph_len += 1
            self.draw()'''

        if global_variables.graph_len_new < len(global_variables.graph_y):

            if global_variables.last != 0:
                global_variables.graph_y_only.append([global_variables.graph_len_new - 1, global_variables.last])

                self.axes.plot(
                    [
                        global_variables.graph_y_only[global_variables.graph_len - 1][0],
                        global_variables.graph_y_only[global_variables.graph_len][0]
                    ],
                    [
                        global_variables.graph_y_only[global_variables.graph_len - 1][1],
                        global_variables.graph_y_only[global_variables.graph_len][1]
                    ],
                    'r')
                global_variables.graph_len += 1
                self.draw()

            global_variables.last = len(global_variables.graph_y) * int(global_variables.size) / global_variables.graph_y[global_variables.graph_len_new]
            global_variables.graph_len_new = len(global_variables.graph_y)
