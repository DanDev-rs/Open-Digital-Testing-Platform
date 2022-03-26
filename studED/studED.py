import sys
# import threading
# import time
# import datetime
# import socket
import json

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog
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


class QPickUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(519, 498)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.desc = QtWidgets.QTextEdit(Form)
        self.desc.setReadOnly(True)
        self.desc.setObjectName("desc")
        self.verticalLayout_2.addWidget(self.desc)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pick1 = QtWidgets.QCheckBox(Form)
        self.pick1.setObjectName("pick1")
        self.verticalLayout.addWidget(self.pick1)
        self.pick2 = QtWidgets.QCheckBox(Form)
        self.pick2.setObjectName("pick2")
        self.verticalLayout.addWidget(self.pick2)
        self.pick3 = QtWidgets.QCheckBox(Form)
        self.pick3.setObjectName("pick3")
        self.verticalLayout.addWidget(self.pick3)
        self.pick4 = QtWidgets.QCheckBox(Form)
        self.pick4.setObjectName("pick4")
        self.verticalLayout.addWidget(self.pick4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pick5 = QtWidgets.QCheckBox(Form)
        self.pick5.setObjectName("pick5")
        self.verticalLayout_3.addWidget(self.pick5)
        self.pick6 = QtWidgets.QCheckBox(Form)
        self.pick6.setObjectName("pick6")
        self.verticalLayout_3.addWidget(self.pick6)
        self.pick7 = QtWidgets.QCheckBox(Form)
        self.pick7.setObjectName("pick7")
        self.verticalLayout_3.addWidget(self.pick7)
        self.pick8 = QtWidgets.QCheckBox(Form)
        self.pick8.setObjectName("pick8")
        self.verticalLayout_3.addWidget(self.pick8)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pick1.setText(_translate("Form", "CheckBox"))
        self.pick2.setText(_translate("Form", "CheckBox"))
        self.pick3.setText(_translate("Form", "CheckBox"))
        self.pick4.setText(_translate("Form", "CheckBox"))
        self.pick5.setText(_translate("Form", "CheckBox"))
        self.pick6.setText(_translate("Form", "CheckBox"))
        self.pick7.setText(_translate("Form", "CheckBox"))
        self.pick8.setText(_translate("Form", "CheckBox"))


class QSingleUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(457, 261)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.desc = QtWidgets.QTextEdit(Form)
        self.desc.setReadOnly(True)
        self.desc.setObjectName("desc")
        self.verticalLayout.addWidget(self.desc)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.answ = QtWidgets.QLineEdit(Form)
        self.answ.setObjectName("answ")
        self.verticalLayout.addWidget(self.answ)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class QEndPageUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.result = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.result.setFont(font)
        self.result.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.result.setText("")
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.result.setObjectName("result")
        self.verticalLayout.addWidget(self.result)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.quit_btn = QtWidgets.QPushButton(Form)
        self.quit_btn.setObjectName("quit_btn")
        self.verticalLayout.addWidget(self.quit_btn)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Тест завершён. Ваш результат:"))
        self.quit_btn.setText(_translate("Form", "Выйти"))


class QMainUi(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(845, 602)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.questions = QtWidgets.QStackedWidget(self.centralwidget)
        self.questions.setEnabled(True)
        self.questions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.questions.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.questions.setLineWidth(4)
        self.questions.setMidLineWidth(2)
        self.questions.setObjectName("questions")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout = QtWidgets.QGridLayout(self.page)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.loadlocal_btn = QtWidgets.QPushButton(self.page)
        self.loadlocal_btn.setMinimumSize(QtCore.QSize(200, 0))
        self.loadlocal_btn.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loadlocal_btn.setFont(font)
        self.loadlocal_btn.setObjectName("loadlocal_btn")
        self.gridLayout.addWidget(self.loadlocal_btn, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.test_name = QtWidgets.QLineEdit(self.page)
        self.test_name.setMinimumSize(QtCore.QSize(300, 30))
        self.test_name.setMaximumSize(QtCore.QSize(700, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.test_name.setFont(font)
        self.test_name.setAlignment(QtCore.Qt.AlignCenter)
        self.test_name.setReadOnly(True)
        self.test_name.setObjectName("test_name")
        self.gridLayout.addWidget(self.test_name, 7, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.start_btn = QtWidgets.QPushButton(self.page)
        self.start_btn.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 8, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 9, 0, 1, 1)
        self.request_btn = QtWidgets.QPushButton(self.page)
        self.request_btn.setMinimumSize(QtCore.QSize(200, 0))
        self.request_btn.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.request_btn.setFont(font)
        self.request_btn.setCheckable(False)
        self.request_btn.setChecked(False)
        self.request_btn.setFlat(False)
        self.request_btn.setObjectName("request_btn")
        self.gridLayout.addWidget(self.request_btn, 1, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.questions.addWidget(self.page)
        self.verticalLayout.addWidget(self.questions)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 21))
        self.menubar.setObjectName("menubar")
        self.editor_menu = QtWidgets.QMenu(self.menubar)
        self.editor_menu.setObjectName("editor_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar_widget = QtWidgets.QDockWidget(MainWindow)
        self.toolbar_widget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable|QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.toolbar_widget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.toolbar_widget.setObjectName("toolbar_widget")
        self.toolbar = QtWidgets.QWidget()
        self.toolbar.setObjectName("toolbar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.toolbar)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.t_counter = QtWidgets.QLabel(self.toolbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.t_counter.sizePolicy().hasHeightForWidth())
        self.t_counter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.t_counter.setFont(font)
        self.t_counter.setFrameShape(QtWidgets.QFrame.Box)
        self.t_counter.setText("")
        self.t_counter.setTextFormat(QtCore.Qt.RichText)
        self.t_counter.setScaledContents(False)
        self.t_counter.setWordWrap(False)
        self.t_counter.setIndent(3)
        self.t_counter.setObjectName("t_counter")
        self.horizontalLayout.addWidget(self.t_counter)
        self.t_time = QtWidgets.QTimeEdit(self.toolbar)
        self.t_time.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(6, 0, 0)))
        self.t_time.setObjectName("t_time")
        self.horizontalLayout.addWidget(self.t_time)
        self.t_finish = QtWidgets.QPushButton(self.toolbar)
        self.t_finish.setObjectName("t_finish")
        self.horizontalLayout.addWidget(self.t_finish)
        self.t_prev = QtWidgets.QPushButton(self.toolbar)
        self.t_prev.setMinimumSize(QtCore.QSize(30, 20))
        self.t_prev.setMaximumSize(QtCore.QSize(70, 16777215))
        self.t_prev.setBaseSize(QtCore.QSize(0, 0))
        self.t_prev.setObjectName("t_prev")
        self.horizontalLayout.addWidget(self.t_prev)
        self.t_next = QtWidgets.QPushButton(self.toolbar)
        self.t_next.setMinimumSize(QtCore.QSize(30, 20))
        self.t_next.setMaximumSize(QtCore.QSize(70, 30))
        self.t_next.setObjectName("t_next")
        self.horizontalLayout.addWidget(self.t_next)
        self.toolbar_widget.setWidget(self.toolbar)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.toolbar_widget)
        self.create_single = QtWidgets.QAction(MainWindow)
        self.create_single.setObjectName("create_single")
        self.create_pick = QtWidgets.QAction(MainWindow)
        self.create_pick.setObjectName("create_pick")
        self.create_pickmulti = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logos/create_pickmulti.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.create_pickmulti.setIcon(icon)
        self.create_pickmulti.setObjectName("create_pickmulti")
        self.save = QtWidgets.QAction(MainWindow)
        self.save.setObjectName("save")
        self.save_as = QtWidgets.QAction(MainWindow)
        self.save_as.setObjectName("save_as")
        self.a_exit = QtWidgets.QAction(MainWindow)
        self.a_exit.setObjectName("a_exit")
        self.testoptions = QtWidgets.QAction(MainWindow)
        self.testoptions.setObjectName("testoptions")
        self.open_test = QtWidgets.QAction(MainWindow)
        self.open_test.setObjectName("open_test")
        self.new_test = QtWidgets.QAction(MainWindow)
        self.new_test.setObjectName("new_test")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.editor_menu.addAction(self.action)
        self.editor_menu.addSeparator()
        self.editor_menu.addAction(self.a_exit)
        self.menubar.addAction(self.editor_menu.menuAction())

        self.retranslateUi(MainWindow)
        self.questions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ОСЦТ - Ученическая версия"))
        self.loadlocal_btn.setText(_translate("MainWindow", "Загрузить с компьютера"))
        self.label.setText(_translate("MainWindow", "ИЛИ"))
        self.start_btn.setText(_translate("MainWindow", "Начать"))
        self.request_btn.setText(_translate("MainWindow", "Запросить у учителя"))
        self.editor_menu.setTitle(_translate("MainWindow", "Опции"))
        self.t_finish.setText(_translate("MainWindow", "Завершить"))
        self.t_prev.setText(_translate("MainWindow", "<<<"))
        self.t_next.setText(_translate("MainWindow", ">>>"))
        self.create_single.setText(_translate("MainWindow", "С одним ответом"))
        self.create_pick.setText(_translate("MainWindow", "С выбором из нескольких ответов"))
        self.create_pickmulti.setText(_translate("MainWindow", "С выбором нескольких ответов"))
        self.save.setText(_translate("MainWindow", "Сохранить"))
        self.save_as.setText(_translate("MainWindow", "Сохранить как"))
        self.a_exit.setText(_translate("MainWindow", "Выход из программы"))
        self.testoptions.setText(_translate("MainWindow", "Параметры теста"))
        self.open_test.setText(_translate("MainWindow", "Открыть тест"))
        self.new_test.setText(_translate("MainWindow", "Новый тест"))
        self.action.setText(_translate("MainWindow", "Настройки подключения"))


class EndPage(QWidget, QEndPageUi):
    def __init__(self):
        super().__init__()
        # uic.loadUi(sys.path[0] + '\\ui\\endpage.ui', self)
        self.setupUi(self)


class SingleTestPage(QWidget, QSingleUi):
    def __init__(self, setup):
        super().__init__()
        # uic.loadUi(sys.path[0] + '\\ui\\q_single.ui', self)
        self.setupUi(self)
        self.desc.setText(setup['desc'])

    def returnanswer(self):
        return self.answ.text()


class PickTestPage(QWidget, QPickUi):
    def __init__(self, setup):
        super().__init__()
        picks = []
        # uic.loadUi(sys.path[0] + '\\ui\\q_pick.ui', self)
        self.setupUi(self)

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


class MainWindow(QMainWindow, QMainUi):
    def __init__(self):
        super().__init__()
        # uic.loadUi(sys.path[0] + '\\ui\\mainwindow.ui', self)
        self.setupUi(self)

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
