from __future__ import unicode_literals
import random
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
        timer.timeout.connect(self.activator)
        timer.start(100)

    def activator(self):
        if global_variables.graph_active:
            self.graph_active()
        else:
            self.graph_not_active()

    def graph_not_active(self):
        self.axes.cla()
        self.axes.plot([0], [0], 'ro')
        self.draw()

    def graph_active(self):
        length = len(global_variables.graph_y)
        self.axes.plot([length - 2, length-1], [global_variables.graph_y[length - 2], global_variables.graph_y[length - 1]], 'r')
        self.draw()
