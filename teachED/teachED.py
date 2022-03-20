# import socket
import schedule
import time
import json
import sqlite3

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QErrorMessage, QMessageBox, \
    QTableWidgetItem


class NoFileName(Exception):
    pass


class UiSetup(object):
    def setupmainui(self, window):
        pass


class SingleTestPage(QWidget, UiSetup):
    def __init__(self, setup=None):
        super().__init__()
        uic.loadUi(sys.path[0] + '\\ui\\q_single.ui', self)
        if setup is not None:
            self.desc.setText(setup['desc'])
            self.answ.setText(setup['answer'])

    def extractcontent(self):
        out = {'type': 'single', 'answer': self.answ.text(), 'desc': self.desc.toPlainText()}
        return out


class PickTestPage(QWidget, UiSetup):
    def __init__(self, setup=None):
        super().__init__()
        picks = []
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

        if setup is not None:
            self.desc.setText(setup['desc'])
            for n in setup['picked']:
                self.picks[n].setCheckState(True)
            for i in range(0, 8):
                self.opts[i].setText(setup['options'][i])

    def extractcontent(self):
        out = {
            'type': 'pick',
            'desc': self.desc.toPlainText(),
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

# TODO: сделать подтверждение удаления
# TODO: ученическая версия
# TODO при открытии теста некоторые галочки меняются на tristate?
# TODO: автообновление (опционально)
# TODO: оценка результатов теста


class MainWindow(QMainWindow, UiSetup):
    def __init__(self):
        super().__init__()
        global tables
        uic.loadUi(sys.path[0] + '\\ui\\mainwindow.ui', self)
        self.bd = sqlite3.connect('results.db')
        for name in self.bd.cursor().execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall():
            tables.append(name[0])
        print(tables)
        self.view_table.setHorizontalHeaderLabels(['Номер', 'Имя', 'Дата и время', 'Результат в %'])
        self.viewindex = 0
        schedule.every(30).seconds.do(self.refresh)

        self.view_name.setText(tables[self.viewindex])
        self.a_exit.triggered.connect(self.exit)
        self.a_toeditor.triggered.connect(self.loadeditor)
        self.f_enable.clicked.connect(self.refresh)
        self.v_right.clicked.connect(self.changetable)
        self.v_left.clicked.connect(self.changetable)
        self.t_refresh.clicked.connect(self.refresh)
        self.refresh()

    def refresh(self):
        global tables

        if self.comp_check.isChecked():
            if self.comp_type.currentIndex() == 0:
                cmp = 0
            else:
                cmp = 1
            completion = self.comp_spin.value()
        else:
            completion = None
        if self.date_check.isChecked():
            dt = self.date_edit.date()
            date = str(dt.day()) + '.' + str(dt.month()) + '.' + str(dt.year())
        else:
            date = None

        if tables:
            self.view_name.setText(tables[self.viewindex])
            self.view_table.clear()
            self.view_table.setRowCount(0)

            bd = sqlite3.connect('results.db')
            cur = bd.cursor()
            print(tables[self.viewindex])
            items = cur.execute('''SELECT * FROM {}'''.format(tables[self.viewindex])).fetchall()
            passed = list()
            for elem in items:
                e_cmp = elem[3]
                e_date = elem[2].split()[0]
                if completion is not None:
                    if date is not None:
                        if cmp == 0:
                            if e_cmp <= completion and e_date == date:
                                passed.append(elem)
                        else:
                            if e_cmp >= completion and e_date == date:
                                passed.append(elem)
                    else:
                        if cmp == 0:
                            if e_cmp <= completion:
                                passed.append(elem)
                        else:
                            if e_cmp >= completion:
                                passed.append(elem)
                elif date is not None:
                    if e_date == date:
                        passed.append(elem)
                else:
                    passed = items

            self.view_table.setRowCount(len(passed))
            if passed:
                for i, f in enumerate(passed):
                    for j, val in enumerate(f):
                        self.view_table.setItem(i, j, QTableWidgetItem(str(val)))
        print(schedule.get_jobs())
        print('refreshed')

    def loadmainwindow(self):
        self.loadeditorwindow(0)

    def changetable(self):
        sender = self.sender()
        global tables
        print(self.viewindex, len(tables))
        if sender == self.v_right:
            if self.viewindex + 1 <= len(tables) - 1:
                self.viewindex += 1
        else:
            if self.viewindex > 0:
                self.viewindex -= 1
        self.refresh()

    def deletetable(self):
        pass

    def loadeditor(self):
        ed.show()
        self.hide()

    @staticmethod
    def exit():
        sys.exit()


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
        self.test_name.editingFinished.connect(self.refresh)

        self.refresh()

    def newtest(self):
        path = QFileDialog.getExistingDirectory(self, 'Новый тест', '')
        print(path)

    def opentest(self):
        tempind = self.questions.count() - 1
        while self.questions.count() > 1:
            self.questions.setCurrentIndex(tempind)
            wd = self.questions.currentWidget()
            self.questions.removeWidget(wd)
            tempind -= 1
        tempind = 0
        path = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '', )[0]
        with open(path, 'r') as jj:
            data = json.load(jj)
        self.timer = data['timer']
        self.testname = data['name']
        self.filename = data['filename']
        for pagedata in data['pages']:
            tempind += 1
            if pagedata['type'] == 'single':
                self.questions.addWidget(SingleTestPage(pagedata))
            else:
                self.questions.addWidget(PickTestPage(pagedata))
        self.test_name.setText(self.testname)
        self.pageindex = 0
        self.refresh()

    def refresh(self):
        print(self.pageindex)
        self.testname = self.test_name.text()
        self.questions.setCurrentIndex(self.pageindex)
        self.test_name.setText(self.testname)
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
        self.refresh()

    def changepage(self):
        sender = self.sender()
        if sender == self.next_page:
            if self.pageindex + 1 <= self.questions.count() - 1:
                self.pageindex += 1
        else:
            if self.pageindex > 0:
                self.pageindex -= 1
        self.refresh()

    def deletepage(self):
        if self.questions.count() > 1:
            self.questions.removeWidget(self.questions.currentWidget())
            self.pageindex -= 1
        else:
            self.delete_page.setDisabled(True)
        self.refresh()

    def __exit__(self):
        dil = QMessageBox()
        dil.setWindowTitle('Выход из редактора')
        dil.setText('Сохранить внесённые изменения?')
        dil.setIcon(QMessageBox.Question)
        savebtn = dil.addButton('Сохранить', QMessageBox.AcceptRole)
        cancelbtn = dil.addButton('Отмена', QMessageBox.NoRole)
        nosavebtn = dil.addButton('Не сохранять', QMessageBox.RejectRole)
        dil.setEscapeButton(cancelbtn)
        dil.show()
        dil.exec()
        c = dil.clickedButton()
        if c == nosavebtn:
            mw.show()
            dil.hide()
            self.hide()
        elif c == savebtn:
            self.savetest()
            mw.show()
            dil.hide()
            self.hide()
        else:
            pass

    def savetest(self):
        global tables
        directory = QFileDialog.getExistingDirectory()

        tl = self.time_limit.time()
        timelim = tl.hour() * 3600 + tl.minute() * 60 + tl.second()
        print(timelim)
        data = {'timer': timelim, 'name': self.testname, 'pages': []}
        for i in range(1, self.questions.count()):
            self.questions.setCurrentIndex(i)
            w = self.questions.currentWidget()
            data['pages'].append(w.extractcontent())
        out_name = '_'.join(g for g in self.testname.split())
        filename = directory + '\\' + out_name + '.json'
        try:
            if directory == '':
                raise NoFileName
            with open(filename, 'w') as f:
                json.dump(data, f)
            print(data)
            if self.testname not in tables:
                bd = sqlite3.connect('results.db')
                bd.cursor().execute('''CREATE TABLE {}
                   (id INT PRIMARY KEY UNIQUE,
                    name TEXT,
                    date DATETIME,
                    completion INT)'''.format(out_name))
                tables.append(out_name)
        except NoFileName:
            pass
        except sqlite3.OperationalError:
            error = QErrorMessage().qtHandler()
            error.showMessage('Нет имени теста!', 'qWarning')
        finally:
            self.refresh()


if __name__ == '__main__':
    tables = list()
    app = QApplication(sys.argv)
    mw = MainWindow()
    ed = EditorWindow()
    mw.show()
    sys.exit(app.exec_())
