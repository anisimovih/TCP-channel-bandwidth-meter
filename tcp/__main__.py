import sys
from PyQt5 import QtCore, QtWidgets
from src.interface_logic import CrossWindow

app = QtWidgets.QApplication(sys.argv)
window = CrossWindow()
window.show()
app.exec_()