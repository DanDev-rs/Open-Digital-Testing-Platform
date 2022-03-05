# import socket
# import schedule
import json
# import sqlite3
# import socket
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QErrorMessage, QMessageBox


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

    def extractcontent(self):
        out = {'answer': self.answ.text(), 'desc': self.desc.toPlainText()}
        return out


class PickTestPage(QWidget, UiSetup):
    def __init__(self, opts=None, picks=None):
        super().__init__()
        if picks is None:
            picks = []
        if opts is None:
            opts = []
        uic.loadUi(sys.path[0] + '\\ui\\q_pick.ui', self)

        self.picks = picks
        self.opts = opts
        self.picks.append(self.pick_1)
        self.picks.append(self.pick_2)
        self.picks.append(self.pick_3)
        self.picks.append(self.pick_4)
        self.picks.append(self.pick_5)
        self.picks.append(self.pick_6)
        self.picks.append(self.pick_7)
        self.picks.append(self.pick_8)

        self.opts.append(self.opt_1)
        self.opts.append(self.opt_2)
        self.opts.append(self.opt_3)
        self.opts.append(self.opt_4)
        self.opts.append(self.opt_5)
        self.opts.append(self.opt_6)
        self.opts.append(self.opt_7)
        self.opts.append(self.opt_8)

    def extractcontent(self):
        out = {
            'options': [],
            'picked': []
        }
        for i in range(0, 8):
            p = self.picks[i]
            o = self.opts[i]
            if p.isChecked():
                out['picked'].append(i)
            if o.text() != '':
                out['options'].append(o.text())
            else:
                out['options'].append(None)
        return out


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

    def loadeditor(self):
        ed.show()
        self.hide()


class EditorWindow(QMainWindow, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\editor.ui', self)
        self.pageindex = 0
        self.timer = 0
        self.testname = 'Новый тест'
        self.filename = None

        self.exit_editor.triggered.connect(self.__exit__)
        self.create_single.triggered.connect(self.createpage)
        self.create_pick.triggered.connect(self.createpage)
        self.new_test.triggered.connect(self.newtest)
        self.open_test.triggered.connect(self.opentest)
        self.save.triggered.connect(self.savetest)
        self.save_as.triggered.connect(self.savetest)
        self.next_page.clicked.connect(self.changepage)
        self.prev_page.clicked.connect(self.changepage)
        self.delete_page.clicked.connect(self.deletepage)

        self.test_name.setText(self.testname)

        self.refresh()

    def newtest(self):
        path = QFileDialog.getExistingDirectory(self, 'Новый тест', '')
        print(path)

    def opentest(self):
        pass

    def refresh(self):
        print(self.pageindex)
        if self.pageindex == 0:
            self.delete_page.setDisabled(True)
            self.prev_page.setDisabled(True)
        else:
            self.prev_page.setDisabled(False)
            self.delete_page.setDisabled(False)
        if self.pageindex + 1 > self.questions.count() - 1:
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
        sender = self.sender()
        if sender == self.next_page:
            if self.pageindex + 1 <= self.questions.count() - 1:
                self.pageindex += 1
        else:
            if self.pageindex > 0:
                self.pageindex -= 1
        self.questions.setCurrentIndex(self.pageindex)
        self.refresh()

    def deletepage(self):
        if self.questions.count() > 1:
            self.questions.removeWidget(self.questions.currentWidget())
            self.pageindex -= 1
        else:
            self.delete_page.setDisabled(True)
        self.refresh()

    def __exit__(self):
        # TODO: допилить и привязать диалог
        dil = QMessageBox()
        dil.setWindowTitle('Выход из редактора')
        dil.setText('Сохранить внесённые изменения?')
        dil.addButton(QMessageBox.StandardButton, QMessageBox.Discard)
        dil.addButton('Сохранить', QMessageBox.Save)
        dil.addButton('Отмена', QMessageBox.Cancel)
        dil.setDefaultButton(QMessageBox.Save)
        dil.setEscapeButton(QMessageBox.Cancel)
        c = dil.clickedButton()
        if c == QMessageBox.Discard:
            mw.show()
            self.hide()
        elif c == QMessageBox.Save:
            self.savetest()
            mw.show()
            self.hide()
        else:
            pass

    def savetest(self):
        if self.sender() == self.save_as or self.filename is None:
            filename = QFileDialog.getSaveFileName(self, 'Сохранить тест', '', '*.json')[0]
        else:
            filename = self.filename
        data = {'timer': self.timer, 'name': self.testname}
        for i in range(1, self.questions.count()):
            self.questions.setCurrentIndex(i)
            w = self.questions.currentWidget()
            data[str(i)] = w.extractcontent()
        if filename != '':
            with open(filename, 'w') as f:
                json.dump(data, f)
            print(data)
        else:
            error = QErrorMessage()
            error.showMessage('Пустое название файла!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    ed = EditorWindow()
    mw.show()
    sys.exit(app.exec_())
