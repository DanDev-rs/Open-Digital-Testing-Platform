import sqlite3
import sys
import socket

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainmenu.ui', self)
        # self.clock =
        self.button_connect.clicked.connect(self.do_update)

    def do_update(self):
        self.label_connect.setText('yes')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
