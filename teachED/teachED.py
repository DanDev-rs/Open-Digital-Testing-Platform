import socket
import schedule
import json
import sqlite3
import socket
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog


class UiSetup(object):
    def setupmainui(self, window):
        pass


class SettingsPage(QWidget, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\q_init.ui', self)
        self.timer = 0


class SingleTestPage(QWidget, UiSetup):
    def __init__(self, text='', answer=''):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\q_single.ui', self)
        self.text = text
        self.answer = answer
        self.desc.setText(self.text)
        self.answ.setText(self.answer)


class PickTestPage(QWidget, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\q_pick.ui', self)


class MainWindow(QMainWindow, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\mainwindow.ui', self)
        self.to_editor.triggered.connect(self.loadeditor)
        self.refresh()

    def refresh(self):
        pass

    def loadmainwindow(self):
        self.loadeditorwindow(0)

    def loadeditor(self, ind=0):
        ed.show()
        self.hide()


class EditorWindow(QMainWindow, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\editor.ui', self)
        self.pageindex = 0
        self.metadata = {'timer': 0, 'name': 'Новый тест'}
        self.exit_editor.triggered.connect(self.__exit__)
        self.create_single.triggered.connect(self.createpage)
        self.create_pick.triggered.connect(self.createpage)
        self.new_test.triggered.connect(self.newtest)
        self.open_test.triggered.connect(self.opentest)
        self.next_page.clicked.connect(self.changepage)
        self.prev_page.clicked.connect(self.changepage)
        self.delete_page.clicked.connect(self.deletepage)
        self.refresh()

    def newtest(self):
        path = QFileDialog.getExistingDirectory(self, 'Новый тест', '')
        print(path)

    def opentest(self):
        pass

    def refresh(self):
        if self.pageindex == 0:
            self.prev_page.setDisabled(True)
            self.delete_page.setDisabled(True)
        else:
            self.prev_page.setDisabled(False)
            self.delete_page.setDisabled(False)
        if self.pageindex == self.questions.count() - 1:
            self.next_page.setDisabled(True)
        else:
            self.next_page.setDisabled(False)

    def createpage(self):
        sender = self.sender()
        self.delete_page.setDisabled(False)
        self.pageindex += 1
        if sender == self.create_single:
            self.questions.addWidget(SingleTestPage())
        else:
            self.questions.addWidget(PickTestPage())
        self.questions.setCurrentIndex(self.pageindex)
        self.refresh()

    def changepage(self):
        pid = self.pageindex
        sender = self.sender()
        if sender == self.next_page:
            if pid + 1 <= self.questions.count() - 1:
                pid += 1
        else:
            if pid > 0:
                pid -= 1
        self.questions.setCurrentIndex(pid)
        print(pid)
        self.refresh()

    def deletepage(self):
        if self.questions.count() > 1:
            self.questions.removeWidget(self.questions.currentWidget())
            self.pageindex -= 1
        else:
            self.delete_page.setDisabled(True)
        self.refresh()

    def __exit__(self):
        self.savetest()
        mw.show()
        self.hide()

    def savetest(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    ed = EditorWindow()
    mw.show()
    sys.exit(app.exec_())
