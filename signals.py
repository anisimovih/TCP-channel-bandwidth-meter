from __future__ import unicode_literals
import sys
import traceback
from PyQt5.QtCore import (QObject, QRunnable, pyqtSignal, pyqtSlot)


class WorkerSignals(QObject):
    """ Определяет сигналы, доступные из рабочего рабочего потока Worker(QRunnable)."""

    finish = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    """ Наследует от QRunnable, настройки рабочего потока обработчика, сигналов и wrap-up. """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Хранить аргументы конструктора (повторно используемые для обработки)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        print("\nfn=`{}`, \nargs=`{}`, kwargs=`{}`, \nself.signals=`{}`"\
              .format(fn, args, kwargs, self.signals))

        # == Добавьте обратный вызов в наши kwargs ====================================###
        kwargs['progress_callback'] = self.signals.progress
        print("kwargs['progress_callback']->`{}`\n".format(kwargs['progress_callback']))

    @pyqtSlot()
    def run(self):
        # Получите args/kwargs здесь; и обработка с их использованием
        try:                       # выполняем метод `execute_this_fn` переданный из Main
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:  # если ошибок не была, испускаем сигнал .result и передаем результат `result`
            self.signals.result.emit(result)      # Вернуть результат обработки
        finally:
            self.signals.finish.emit()            # Done / Готово
