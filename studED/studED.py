import sys
import threading
import time
import datetime
import socket
import json

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog, QErrorMessage
# TODO: интерфейс
# TODO: связь с компьютером учителя через сокет
# TODO: отправка результата и получение тестов по сети
# TODO: рабочий таймер через threading


def decode(word, codekey):
    letters = list(word.strip())
    opers = list()
    out = list()
    for n in range(0, 11, 2):
        opers.append((int(codekey[n]), int(codekey[n + 1])))
    for lt in letters:
        ind = ord(lt)
        for oper in opers:
            op, num = oper
            if op in {1, 3, 4, 6}:
                ind -= num
            elif op in {2, 5, 7, 8}:
                ind += num
        out.append(ind)
    return ''.join(chr(g) for g in out)


class UiSetup(object):
    def setupmainui(self, window):
        pass


class EndPage(QWidget, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\endpage.ui', self)


class SingleTestPage(QWidget, UiSetup):
    def __init__(self, setup):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\q_single.ui', self)
        self.desc.setText(setup['desc'])

    def returnanswer(self):
        return self.answ.text()


class PickTestPage(QWidget, UiSetup):
    def __init__(self, setup):
        super().__init__()
        picks = []
        uic.loadUi(sys.path[0] + '\\ui\\q_pick.ui', self)

        self.picks = picks
        self.picks.append(self.pick1)
        self.picks.append(self.pick2)
        self.picks.append(self.pick3)
        self.picks.append(self.pick4)
        self.picks.append(self.pick5)
        self.picks.append(self.pick6)
        self.picks.append(self.pick7)
        self.picks.append(self.pick8)

        self.desc.setText(setup['desc'])
        for n in range(0, 8):
            p = self.picks[n]
            if setup['options'][n] is None:
                p.hide()
            else:
                p.setText(setup['options'][n])

    def returnanswer(self):
        out = ''
        for i in range(0, 8):
            p = self.picks[i]
            if p.isChecked():
                out += '1'
            else:
                out += '0'
        return out


class MainWindow(QMainWindow, UiSetup):
    def __init__(self):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\mainwindow.ui', self)

        tempind = self.questions.count() - 1
        while self.questions.count() > 1:
            self.questions.setCurrentIndex(tempind)
            wd = self.questions.currentWidget()
            self.questions.removeWidget(wd)
            tempind -= 1

        self.pageindex = 0
        self.timer = 0
        self.filename = None
        self.testname = None
        self.testactive = False
        self.codekey = None
        self.data = None
        self.toolbar_widget.hide()

        self.start_btn.clicked.connect(self.begintest)
        self.loadlocal_btn.clicked.connect(self.opentest)
        self.t_finish.clicked.connect(self.finishtest)
        self.t_next.clicked.connect(self.changepage)
        self.t_prev.clicked.connect(self.changepage)
        self.a_exit.triggered.connect(self.__exit__)
        self.test_name.clear()
        self.start_btn.setDisabled(True)
        self.request_btn.setDisabled(True)
        self.t_next.setDisabled(True)
        self.t_prev.setDisabled(True)
        self.t_finish.setDisabled(True)

    def opentest(self):
        tempind = 1
        path = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '')[0]
        if path != '':
            with open(path, 'r') as jj:
                data = json.load(jj)
            self.data = data
            self.timer = data['timer']
            self.testname = data['name']
            self.codekey = data['codekey']
            self.test_name.setText(self.testname)
            for pagedata in data['pages']:
                tempind += 1
                if pagedata['type'] == 'single':
                    self.questions.addWidget(SingleTestPage(pagedata))
                else:
                    self.questions.addWidget(PickTestPage(pagedata))
            self.start_btn.setDisabled(False)
            self.pageindex = 0

    def refresh(self):
        print(self.pageindex)
        self.questions.setCurrentIndex(self.pageindex)
        if self.pageindex == 1:
            self.t_prev.setDisabled(True)
        else:
            self.t_prev.setDisabled(False)
        if self.pageindex + 1 > self.questions.count() - 1:
            self.t_next.setDisabled(True)
        else:
            self.t_next.setDisabled(False)
        self.t_counter.setText('Вопрос ' + str(self.pageindex) + ' из ' + str(self.questions.count() - 1))

    def changepage(self):
        sender = self.sender()
        if sender == self.t_next:
            if self.pageindex + 1 <= self.questions.count() - 1:
                self.pageindex += 1
        else:
            if self.pageindex > 1:
                self.pageindex -= 1
        self.refresh()

    def __exit__(self):
        if self.testactive:
            dil = QMessageBox()
            dil.setWindowTitle('Выход из тестировщика')
            dil.setText('Вы уверены? Весь ваш прогресс будет утерян!')
            dil.setIcon(QMessageBox.Question)
            exitbtn = dil.addButton('Выход', QMessageBox.AcceptRole)
            cancelbtn = dil.addButton('Отмена', QMessageBox.RejectRole)
            dil.setEscapeButton(cancelbtn)
            dil.show()
            dil.exec()
            c = dil.clickedButton()
            if c == exitbtn:
                sys.exit()
            elif c == cancelbtn:
                pass
        else:
            sys.exit()

    def begintest(self):
        self.t_next.setDisabled(False)
        self.t_prev.setDisabled(False)
        self.t_finish.setDisabled(False)
        self.toolbar_widget.show()
        self.pageindex = 1
        self.testactive = True
        self.refresh()

    def finishtest(self):
        total = 0
        allq = self.questions.count() - 1
        for i in range(1, self.questions.count()):
            self.questions.setCurrentIndex(i)
            wd = self.questions.currentWidget()
            a1 = wd.returnanswer()
            a2 = decode(self.data['pages'][i - 1]['answer'], self.codekey)
            print(a1, a2)
            if a1 == a2:
                total += 1

        tempind = self.questions.count() - 1
        while self.questions.count() > 1:
            self.questions.setCurrentIndex(tempind)
            wd = self.questions.currentWidget()
            self.questions.removeWidget(wd)
            tempind -= 1

        self.questions.insertWidget(1, EndPage())
        self.questions.setCurrentIndex(1)
        self.toolbar_widget.hide()
        endw = self.questions.currentWidget()
        endw.result.setText(str(total) + ' вопросов из ' + str(allq))
        endw.quit_btn.clicked.connect(self.__exit__)
        self.testactive = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
