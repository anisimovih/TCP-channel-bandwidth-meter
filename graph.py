from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from matplotlib.pyplot import plot
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import global_variables
from scipy.interpolate import UnivariateSpline, Akima1DInterpolator, PchipInterpolator
import numpy as np

'''class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)'''


class Graph(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""

    normal_speeds_quantity = 0  # Общее количество нормальных значений
    normal_speeds_number = 0  # Количество уже отображенных значений
    speed_limit = 10000  # Ограничение скорости для отсечения аномальных значений
    graph_x = np.array([0])
    graph_y = np.array([0])
    graph_active = False  # Активность графика.

    def __init__(self, *args, **kwargs):
        self.fig = plt.figure(figsize=(4, 5))
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)  # (n_rows, n_cols, index)

        """Переменные для перемещения/иприближения графика"""
        self.selecting = False
        self.start_x = None
        self.start_y = None
        self.select_width = None  # Ширина последнего выделения, если курсор пересечет границу
        self.select_height = None  # Высота последнего выделения, если курсор пересечет границу
        self.select_rect = self.axes.add_patch(self.rectangle(0, 0, 0, 0))
        self.cur_xlim = None
        self.cur_ylim = None
        self.auto_limit = False
        self.limit_x_max = 100
        self.limit_y_max = 100

        self.line = None  # График скорости
        #self.draw_start_point()
        self.start_setup()
        timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.draw_graph)
        timer.timeout.connect(self.test)
        timer.start(3000)

    '''def draw_start_point(self):
        self.axes.grid(axis='both')
        self.line = self.axes.plot([0], [0], 'ro')
        self.axes.set_xlabel("Номер сообщения")
        self.axes.set_ylabel("Скорость (бит/сек)")
        self.axes.set_xlim(xmin=0, xmax=10)
        self.axes.set_ylim(ymin=0, ymax=10)
        self.axes.set_xlim(auto=True)
        self.axes.set_ylim(auto=True)
        self.axes.set_facecolor('xkcd:black')
        self.draw()'''

    def start_setup(self):
        def draw_start_point():
            self.line = self.axes.plot([0], [0], 'ro')
            self.axes.grid(axis='both')
            self.axes.set_xlabel("Номер сообщения")
            self.axes.set_ylabel("Скорость (бит/сек)")

        def setup_axe_limits():
            self.axes.set_xlim(xmin=0, xmax=10)
            self.axes.set_ylim(ymin=0, ymax=10)
            self.axes.set_xlim(auto=True)
            self.axes.set_ylim(auto=True)
            self.fig.subplots_adjust(bottom=0.15, top=0.95, left=0.1, right=0.95)

        def setup_colours():
            #self.axes.set_facecolor('xkcd:black')
            pass

        draw_start_point()
        setup_axe_limits()
        setup_colours()
        self.draw()

    def draw_graph(self):
        if Graph.graph_active:
            if Graph.normal_speeds_number < Graph.normal_speeds_quantity:
                self.line.pop(0).remove()
                bi = PchipInterpolator(Graph.graph_x, Graph.graph_y)
                x_smooth = np.linspace(min(Graph.graph_x), max(Graph.graph_x), len(Graph.graph_y) * 10)
                y_smooth = bi(x_smooth)
                self.line = self.axes.plot(x_smooth, y_smooth, 'r')
                self.draw()
                Graph.normal_speeds_number += 1

    # TODO: удалить
    def test(self):
        if Graph.graph_active:
            self.line.pop(0).remove()
            global_variables.graph_smooth_x.append(4 + len(global_variables.graph_smooth_x))
            global_variables.graph_smooth_y.append(len(global_variables.graph_smooth_x))
            self.line = self.axes.plot(global_variables.graph_smooth_x, global_variables.graph_smooth_y, 'r')
            self.axes.set_xlabel("Номер сообщения")
            self.axes.set_ylabel("Скорость (бит/сек)")
            self.draw()
            self.limit_x_max = max(global_variables.graph_smooth_x)
            self.limit_y_max = max(global_variables.graph_smooth_y)

    @staticmethod
    def rectangle(x, y, width, height):
        return patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='blue', alpha=.25)

    def select_start(self, event):
        self.selecting = True
        self.start_x = event.xdata
        self.start_y = event.ydata

    def select_stop(self, event):
        if self.selecting:
            self.selecting = False
            self.select_rect.remove()
            if event.xdata - self.start_x < 1 or event.ydata - self.start_y < 1:
                print("Приближение ближе", 1, "запрещено! (X =", event.xdata - self.start_x, "; Y =", event.ydata - self.start_y, ")")
            else:
                self.axes.set_xlim(xmin=self.start_x, xmax=event.xdata)
                self.axes.set_ylim(ymin=self.start_y, ymax=event.ydata)
            self.draw()
            self.select_rect = self.axes.add_patch(Graph.rectangle(0, 0, 0, 0))

    def select_update(self, event):
        if self.selecting:
            if event.xdata is not None:
                self.select_rect.remove()
                self.select_width = event.xdata - self.start_x
                self.select_height = event.ydata - self.start_y
                self.select_rect = self.axes.add_patch(
                    Graph.rectangle(self.start_x, self.start_y, self.select_width,
                                    event.ydata - self.start_y))
                self.draw()
            else:
                self.select_rect.remove()
                self.select_rect = self.axes.add_patch(
                    Graph.rectangle(self.start_x, self.start_y, self.select_width,
                                    self.select_height))
                self.draw()

    def zoom(self, event, ax, base_scale=2.):
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        if event.button == 'up':  # zoom in
            scale_factor = 1 / base_scale
        else:  # zoom out
            if self.auto_limit:
                ax.set_xlim(auto=True)
                ax.set_ylim(auto=True)
                ax.figure.canvas.draw()
                return
            scale_factor = base_scale

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - event.xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - event.ydata) / (cur_ylim[1] - cur_ylim[0])

        if event.xdata + new_width * relx < self.limit_x_max and event.ydata + new_height * rely < self.limit_y_max:
            self.auto_limit = False
            ax.set_xlim([event.xdata - new_width * (1 - relx), event.xdata + new_width * relx])
            ax.set_ylim([event.ydata - new_height * (1 - rely), event.ydata + new_height * rely])
        else:
            self.auto_limit = True
            ax.set_xlim(auto=True)
            ax.set_ylim(auto=True)
            ax.margins(0.1, 0.1)
        ax.figure.canvas.draw()

    def pull_start(self, event):
        self.selecting = True
        self.start_x = event.xdata
        self.start_y = event.ydata
        self.cur_xlim = self.axes.get_xlim()
        self.cur_ylim = self.axes.get_ylim()

    def pull_stop(self, event):
        self.selecting = False
        self.draw()

    def pull_update(self, event):
        if not self.selecting:
            return
        if event.inaxes != self.axes:
            return
        dx = event.xdata - self.start_x
        dy = event.ydata - self.start_y
        self.cur_xlim -= dx
        self.cur_ylim -= dy
        self.axes.set_xlim(self.cur_xlim)
        self.axes.set_ylim(self.cur_ylim)
        self.draw()
