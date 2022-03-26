# import socket
# import threading
# import time
import random
import json
import sqlite3

import sys
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QTableWidgetItem


def deencode(word, codekey, decode):
    letters = list(word.strip())
    opers = list()
    out = list()
    for n in range(0, 11, 2):
        opers.append((int(codekey[n]), int(codekey[n + 1])))
    print(opers)
    if decode:
        for lt in letters:
            ind = ord(lt)
            for oper in opers:
                op, num = oper
                if op in {1, 3, 4, 6}:
                    ind -= num
                elif op in {2, 5, 7, 8}:
                    ind += num
            out.append(ind)
    else:
        for lt in letters:
            ind = ord(lt)
            for oper in opers:
                op, num = oper
                if op in {1, 3, 4, 6}:
                    ind += num
                elif op in {2, 5, 7, 8}:
                    ind -= num
            out.append(ind)
    return ''.join(chr(g) for g in out)


class NoFileName(Exception):
    pass


class MainWdUi(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1012, 623)
        MainWindow.setMinimumSize(QtCore.QSize(932, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.view_name = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.view_name.sizePolicy().hasHeightForWidth())
        self.view_name.setSizePolicy(sizePolicy)
        self.view_name.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.view_name.setFont(font)
        self.view_name.setMaxLength(400)
        self.view_name.setFrame(True)
        self.view_name.setDragEnabled(False)
        self.view_name.setReadOnly(True)
        self.view_name.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.view_name.setClearButtonEnabled(False)
        self.view_name.setObjectName("view_name")
        self.horizontalLayout_2.addWidget(self.view_name)
        self.t_delete = QtWidgets.QToolButton(self.centralwidget)
        self.t_delete.setMinimumSize(QtCore.QSize(32, 32))
        self.t_delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../data/icons8-delete-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.t_delete.setIcon(icon)
        self.t_delete.setIconSize(QtCore.QSize(30, 30))
        self.t_delete.setAutoRepeat(False)
        self.t_delete.setObjectName("t_delete")
        self.horizontalLayout_2.addWidget(self.t_delete)
        self.t_refresh = QtWidgets.QToolButton(self.centralwidget)
        self.t_refresh.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/logos/refresh-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("../data/refresh-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.t_refresh.setIcon(icon1)
        self.t_refresh.setIconSize(QtCore.QSize(30, 30))
        self.t_refresh.setAutoRaise(False)
        self.t_refresh.setObjectName("t_refresh")
        self.horizontalLayout_2.addWidget(self.t_refresh)
        self.v_left = QtWidgets.QToolButton(self.centralwidget)
        self.v_left.setAutoFillBackground(False)
        self.v_left.setIconSize(QtCore.QSize(32, 32))
        self.v_left.setAutoRaise(False)
        self.v_left.setArrowType(QtCore.Qt.LeftArrow)
        self.v_left.setObjectName("v_left")
        self.horizontalLayout_2.addWidget(self.v_left)
        self.v_right = QtWidgets.QToolButton(self.centralwidget)
        self.v_right.setIconSize(QtCore.QSize(32, 32))
        self.v_right.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.v_right.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.v_right.setAutoRaise(False)
        self.v_right.setArrowType(QtCore.Qt.RightArrow)
        self.v_right.setObjectName("v_right")
        self.horizontalLayout_2.addWidget(self.v_right)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.view_table = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.view_table.setFont(font)
        self.view_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.view_table.setDragDropOverwriteMode(False)
        self.view_table.setShowGrid(True)
        self.view_table.setColumnCount(4)
        self.view_table.setObjectName("view_table")
        self.view_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.view_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.view_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.view_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.view_table.setHorizontalHeaderItem(3, item)
        self.view_table.horizontalHeader().setVisible(True)
        self.view_table.horizontalHeader().setCascadingSectionResizes(True)
        self.view_table.horizontalHeader().setDefaultSectionSize(140)
        self.view_table.horizontalHeader().setMinimumSectionSize(45)
        self.view_table.horizontalHeader().setSortIndicatorShown(True)
        self.view_table.horizontalHeader().setStretchLastSection(True)
        self.view_table.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.view_table)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1012, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.con_widget_dock = QtWidgets.QDockWidget(MainWindow)
        self.con_widget_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.con_widget_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.con_widget_dock.setObjectName("con_widget_dock")
        self.con_widget = QtWidgets.QWidget()
        self.con_widget.setObjectName("con_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.con_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.con_view = QtWidgets.QListWidget(self.con_widget)
        self.con_view.setObjectName("con_view")
        self.verticalLayout.addWidget(self.con_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.disconnect_button = QtWidgets.QPushButton(self.con_widget)
        self.disconnect_button.setObjectName("disconnect_button")
        self.horizontalLayout.addWidget(self.disconnect_button)
        self.remove_button = QtWidgets.QPushButton(self.con_widget)
        self.remove_button.setObjectName("remove_button")
        self.horizontalLayout.addWidget(self.remove_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.con_widget_dock.setWidget(self.con_widget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.con_widget_dock)
        self.filter_widget = QtWidgets.QDockWidget(MainWindow)
        self.filter_widget.setFloating(False)
        self.filter_widget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.filter_widget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.filter_widget.setObjectName("filter_widget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.comp_check = QtWidgets.QCheckBox(self.frame)
        self.comp_check.setObjectName("comp_check")
        self.verticalLayout_3.addWidget(self.comp_check)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comp_type = QtWidgets.QComboBox(self.frame)
        self.comp_type.setObjectName("comp_type")
        self.comp_type.addItem("")
        self.comp_type.addItem("")
        self.horizontalLayout_4.addWidget(self.comp_type)
        self.comp_spin = QtWidgets.QSpinBox(self.frame)
        self.comp_spin.setObjectName("comp_spin")
        self.horizontalLayout_4.addWidget(self.comp_spin)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.date_check = QtWidgets.QCheckBox(self.frame_2)
        self.date_check.setObjectName("date_check")
        self.verticalLayout_4.addWidget(self.date_check)
        self.date_edit = QtWidgets.QDateEdit(self.frame_2)
        self.date_edit.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 1, 1), QtCore.QTime(0, 0, 0)))
        self.date_edit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2010, 1, 1), QtCore.QTime(0, 0, 0)))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setObjectName("date_edit")
        self.verticalLayout_4.addWidget(self.date_edit)
        self.verticalLayout_5.addWidget(self.frame_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.f_enable = QtWidgets.QPushButton(self.dockWidgetContents)
        self.f_enable.setObjectName("f_enable")
        self.verticalLayout_5.addWidget(self.f_enable)
        self.filter_widget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.filter_widget)
        self.a_exit = QtWidgets.QAction(MainWindow)
        self.a_exit.setObjectName("a_exit")
        self.a_toeditor = QtWidgets.QAction(MainWindow)
        self.a_toeditor.setObjectName("a_toeditor")
        self.a_autoref = QtWidgets.QAction(MainWindow)
        self.a_autoref.setCheckable(True)
        self.a_autoref.setChecked(False)
        self.a_autoref.setObjectName("a_autoref")
        self.menu.addAction(self.a_toeditor)
        self.menu.addSeparator()
        self.menu.addAction(self.a_exit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ОСЦТ - Учительская версия"))
        self.v_left.setText(_translate("MainWindow", "..."))
        self.v_right.setText(_translate("MainWindow", "..."))
        self.view_table.setSortingEnabled(True)
        item = self.view_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер"))
        item = self.view_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Имя участника"))
        item = self.view_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Дата участия"))
        item = self.view_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Процент завершения"))
        self.menu.setTitle(_translate("MainWindow", "Опции"))
        self.con_widget_dock.setWindowTitle(_translate("MainWindow", "Подключенные ученики"))
        self.disconnect_button.setText(_translate("MainWindow", "Отключить..."))
        self.remove_button.setText(_translate("MainWindow", "Удалить..."))
        self.filter_widget.setWindowTitle(_translate("MainWindow", "Фильтры"))
        self.comp_check.setText(_translate("MainWindow", "Процент прохождения"))
        self.comp_type.setItemText(0, _translate("MainWindow", "≤"))
        self.comp_type.setItemText(1, _translate("MainWindow", "≥"))
        self.date_check.setText(_translate("MainWindow", "Дата прохождения"))
        self.f_enable.setText(_translate("MainWindow", "Применить"))
        self.a_exit.setText(_translate("MainWindow", "Выйти из программы"))
        self.a_toeditor.setText(_translate("MainWindow", "Перейти в редактор"))
        self.a_autoref.setText(_translate("MainWindow", "Автообновление"))


class EditorWdUi(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
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
        self.setup_page = QtWidgets.QWidget()
        self.setup_page.setObjectName("setup_page")
        self.gridLayout = QtWidgets.QGridLayout(self.setup_page)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.setup_page)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.time_limit = QtWidgets.QTimeEdit(self.setup_page)
        self.time_limit.setTime(QtCore.QTime(0, 10, 0))
        self.time_limit.setObjectName("time_limit")
        self.gridLayout.addWidget(self.time_limit, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.setup_page)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.test_name = QtWidgets.QLineEdit(self.setup_page)
        self.test_name.setObjectName("test_name")
        self.gridLayout.addWidget(self.test_name, 2, 2, 1, 1)
        self.questions.addWidget(self.setup_page)
        self.verticalLayout.addWidget(self.questions)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prev_page = QtWidgets.QPushButton(self.centralwidget)
        self.prev_page.setObjectName("prev_page")
        self.horizontalLayout_2.addWidget(self.prev_page)
        self.delete_page = QtWidgets.QPushButton(self.centralwidget)
        self.delete_page.setObjectName("delete_page")
        self.horizontalLayout_2.addWidget(self.delete_page)
        self.next_page = QtWidgets.QPushButton(self.centralwidget)
        self.next_page.setObjectName("next_page")
        self.horizontalLayout_2.addWidget(self.next_page)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.editor_menu = QtWidgets.QMenu(self.menubar)
        self.editor_menu.setObjectName("editor_menu")
        self.create_question = QtWidgets.QMenu(self.editor_menu)
        self.create_question.setObjectName("create_question")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        self.exit_editor = QtWidgets.QAction(MainWindow)
        self.exit_editor.setObjectName("exit_editor")
        self.testoptions = QtWidgets.QAction(MainWindow)
        self.testoptions.setObjectName("testoptions")
        self.open_test = QtWidgets.QAction(MainWindow)
        self.open_test.setObjectName("open_test")
        self.new_test = QtWidgets.QAction(MainWindow)
        self.new_test.setObjectName("new_test")
        self.create_question.addAction(self.create_single)
        self.create_question.addAction(self.create_pick)
        self.editor_menu.addAction(self.create_question.menuAction())
        self.editor_menu.addSeparator()
        self.editor_menu.addAction(self.new_test)
        self.editor_menu.addAction(self.open_test)
        self.editor_menu.addAction(self.save)
        self.editor_menu.addAction(self.save_as)
        self.editor_menu.addSeparator()
        self.editor_menu.addAction(self.exit_editor)
        self.menubar.addAction(self.editor_menu.menuAction())

        self.retranslateUi(MainWindow)
        self.questions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OTS - редактор тестов"))
        self.label_2.setText(_translate("MainWindow", "Название теста"))
        self.time_limit.setDisplayFormat(_translate("MainWindow", "H:mm:ss"))
        self.label.setText(_translate("MainWindow", "Установить ограничение по времени\n"
" (0 - без ограничения)"))
        self.test_name.setText(_translate("MainWindow", "Новый тест"))
        self.prev_page.setText(_translate("MainWindow", "<<<"))
        self.delete_page.setText(_translate("MainWindow", "Удалить"))
        self.delete_page.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.next_page.setText(_translate("MainWindow", ">>>"))
        self.editor_menu.setTitle(_translate("MainWindow", "Редактор"))
        self.create_question.setTitle(_translate("MainWindow", "Новый вопрос"))
        self.create_single.setText(_translate("MainWindow", "С одним ответом"))
        self.create_pick.setText(_translate("MainWindow", "С выбором из нескольких ответов"))
        self.create_pickmulti.setText(_translate("MainWindow", "С выбором нескольких ответов"))
        self.save.setText(_translate("MainWindow", "Сохранить"))
        self.save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.save_as.setText(_translate("MainWindow", "Сохранить как"))
        self.save_as.setShortcut(_translate("MainWindow", "Ctrl+Alt+S"))
        self.exit_editor.setText(_translate("MainWindow", "Выйти из редактора"))
        self.exit_editor.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.testoptions.setText(_translate("MainWindow", "Параметры теста"))
        self.open_test.setText(_translate("MainWindow", "Открыть тест"))
        self.open_test.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.new_test.setText(_translate("MainWindow", "Новый тест"))
        self.new_test.setShortcut(_translate("MainWindow", "Ctrl+N"))


class PickQUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(519, 498)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.desc = QtWidgets.QTextEdit(Form)
        self.desc.setObjectName("desc")
        self.verticalLayout.addWidget(self.desc)
        self.hl = QtWidgets.QHBoxLayout()
        self.hl.setObjectName("hl")
        self.fl2 = QtWidgets.QFormLayout()
        self.fl2.setObjectName("fl2")
        self.pick_1 = QtWidgets.QCheckBox(Form)
        self.pick_1.setText("")
        self.pick_1.setIconSize(QtCore.QSize(20, 20))
        self.pick_1.setAutoRepeat(False)
        self.pick_1.setTristate(False)
        self.pick_1.setObjectName("pick_1")
        self.fl2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pick_1)
        self.pick_2 = QtWidgets.QCheckBox(Form)
        self.pick_2.setText("")
        self.pick_2.setTristate(False)
        self.pick_2.setObjectName("pick_2")
        self.fl2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pick_2)
        self.pick_3 = QtWidgets.QCheckBox(Form)
        self.pick_3.setText("")
        self.pick_3.setObjectName("pick_3")
        self.fl2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pick_3)
        self.pick_4 = QtWidgets.QCheckBox(Form)
        self.pick_4.setText("")
        self.pick_4.setObjectName("pick_4")
        self.fl2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pick_4)
        self.opt_1 = QtWidgets.QLineEdit(Form)
        self.opt_1.setObjectName("opt_1")
        self.fl2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.opt_1)
        self.opt_2 = QtWidgets.QLineEdit(Form)
        self.opt_2.setObjectName("opt_2")
        self.fl2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_2)
        self.opt_3 = QtWidgets.QLineEdit(Form)
        self.opt_3.setObjectName("opt_3")
        self.fl2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.opt_3)
        self.opt_4 = QtWidgets.QLineEdit(Form)
        self.opt_4.setObjectName("opt_4")
        self.fl2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.opt_4)
        self.hl.addLayout(self.fl2)
        self.fl1 = QtWidgets.QFormLayout()
        self.fl1.setObjectName("fl1")
        self.pick_5 = QtWidgets.QCheckBox(Form)
        self.pick_5.setText("")
        self.pick_5.setIconSize(QtCore.QSize(20, 20))
        self.pick_5.setAutoRepeat(False)
        self.pick_5.setTristate(False)
        self.pick_5.setObjectName("pick_5")
        self.fl1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pick_5)
        self.opt_5 = QtWidgets.QLineEdit(Form)
        self.opt_5.setObjectName("opt_5")
        self.fl1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.opt_5)
        self.pick_6 = QtWidgets.QCheckBox(Form)
        self.pick_6.setText("")
        self.pick_6.setObjectName("pick_6")
        self.fl1.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pick_6)
        self.opt_6 = QtWidgets.QLineEdit(Form)
        self.opt_6.setObjectName("opt_6")
        self.fl1.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_6)
        self.pick_7 = QtWidgets.QCheckBox(Form)
        self.pick_7.setText("")
        self.pick_7.setObjectName("pick_7")
        self.fl1.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pick_7)
        self.opt_7 = QtWidgets.QLineEdit(Form)
        self.opt_7.setObjectName("opt_7")
        self.fl1.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.opt_7)
        self.pick_8 = QtWidgets.QCheckBox(Form)
        self.pick_8.setText("")
        self.pick_8.setObjectName("pick_8")
        self.fl1.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pick_8)
        self.opt_8 = QtWidgets.QLineEdit(Form)
        self.opt_8.setObjectName("opt_8")
        self.fl1.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.opt_8)
        self.hl.addLayout(self.fl1)
        self.verticalLayout.addLayout(self.hl)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class SingleQUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(457, 261)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.desc = QtWidgets.QTextEdit(Form)
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


class SingleTestPage(QWidget, SingleQUi):
    def __init__(self, code=None, setup=None):
        super().__init__()
        self.setupUi(self)
        # uic.loadUi(sys.path[0] + '\\ui\\q_single.ui', self)
        if setup is not None:
            self.desc.setText(setup['desc'])
            self.answ.setText(deencode(setup['answer'], code, True))

    def extractcontent(self):
        out = {'type': 'single', 'answer': self.answ.text(), 'desc': self.desc.toPlainText()}
        return out


class PickTestPage(QWidget, PickQUi):
    def __init__(self, code=None, setup=None):
        super().__init__()
        picks = []
        opts = []
        # uic.loadUi(sys.path[0] + '\\ui\\q_pick.ui', self)
        self.setupUi(self)

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
            answer = list(deencode(setup['answer'], code, True))
            for i in range(0, 8):
                self.opts[i].setText(setup['options'][i])
                self.picks[i].setTristate(False)
                if answer[i] == '1':
                    self.picks[i].setCheckState(QtCore.Qt.Checked)
                else:
                    self.picks[i].setCheckState(QtCore.Qt.Unchecked)

    def extractcontent(self):
        out = {
            'type': 'pick',
            'desc': self.desc.toPlainText(),
            'options': [],
            'answer': ''
        }
        for i in range(0, 8):
            p = self.picks[i]
            o = self.opts[i]
            if p.isChecked():
                out['answer'] += '1'
            else:
                out['answer'] += '0'
            if o.text() != '':
                out['options'].append(o.text())
            else:
                out['options'].append(None)
        return out

# TODO: сделать подтверждение удаления
# TODO: ученическая версия
# TODO: автообновление (опционально)
# TODO: оценка результатов теста


class MainWindow(QMainWindow, MainWdUi):
    def __init__(self):
        super().__init__()
        global tables
        # uic.loadUi(sys.path[0] + '\\ui\\mainwindow.ui', self)
        self.setupUi(self)
        self.bd = sqlite3.connect('results.db')
        for name in self.bd.cursor().execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall():
            tables.append(name[0])
        tables.sort()
        self.view_table.setHorizontalHeaderLabels(['Номер', 'Имя', 'Дата и время', 'Результат в %'])
        self.viewindex = 0

        self.view_name.setText(tables[self.viewindex])
        self.a_exit.triggered.connect(self.__exit__)
        self.a_toeditor.triggered.connect(self.loadeditor)
        self.f_enable.clicked.connect(self.refresh)
        self.v_right.clicked.connect(self.changetable)
        self.v_left.clicked.connect(self.changetable)
        self.t_refresh.clicked.connect(self.refresh)
        self.t_delete.clicked.connect(self.deletetable)
        if len(tables) > 1:
            self.viewindex = 1
            self.refresh()

    def refresh(self):
        global tables
        cmp = 1
        if self.comp_check.isChecked():
            if self.comp_type.currentIndex() == 0:
                cmp = 0
            completion = self.comp_spin.value()
        else:
            completion = None
        if self.date_check.isChecked():
            dt = self.date_edit.date()
            date = str(dt.day()) + '.' + str(dt.month()) + '.' + str(dt.year())
        else:
            date = None

        if len(tables) > 1:
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
            if self.viewindex > 1:
                self.viewindex -= 1
        self.refresh()

    def deletetable(self):
        if len(tables) > 1:
            self.bd.cursor().execute("""DROP TABLE {}""".format(tables[self.viewindex]))
            tables.pop(self.viewindex)
            if self.viewindex < len(tables) - 1:
                self.viewindex += 1
            else:
                self.viewindex -= 1
            if len(tables) == 1:
                self.viewindex = 0
            self.refresh()

    def loadeditor(self):
        ed.show()
        self.hide()

    def __exit__(self):
        sys.exit()


class EditorWindow(QMainWindow, EditorWdUi):
    def __init__(self):
        super().__init__()
        # uic.loadUi(sys.path[0] + '\\ui\\editor.ui', self)
        self.setupUi(self)
        self.pageindex = 0
        self.timer = 0
        self.testname = 'Новый тест'
        self.filename = None
        self.codekey = None

        tempind = self.questions.count() - 1
        while self.questions.count() > 1:
            self.questions.setCurrentIndex(tempind)
            wd = self.questions.currentWidget()
            self.questions.removeWidget(wd)
            tempind -= 1

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
        if path != '':
            tempind = self.questions.count() - 1
            while self.questions.count() > 1:
                self.questions.setCurrentIndex(tempind)
                wd = self.questions.currentWidget()
                self.questions.removeWidget(wd)
                tempind -= 1
            self.testname = 'Новый тест'
            self.test_name.setText(self.testname)
            self.pageindex = 0
            self.timer = '0:10:00'
            self.codekey = None
            self.time_limit.setTime(QtCore.QTime.fromString(self.timer))
            self.filename = path

    def opentest(self):
        tempind = self.questions.count() - 1
        while self.questions.count() > 1:
            self.questions.setCurrentIndex(tempind)
            wd = self.questions.currentWidget()
            self.questions.removeWidget(wd)
            tempind -= 1
        tempind = 0
        path = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '', '*.json')[0]
        if path != '':
            self.filename = '\\'.join(g for g in list(filter(lambda x: '.json' not in x, path.split('/'))))
            with open(path, 'r') as jj:
                data = json.load(jj)
            self.timer = data['timer']
            self.testname = data['name']
            self.codekey = data['codekey']
            for pagedata in data['pages']:
                tempind += 1
                if pagedata['type'] == 'single':
                    self.questions.addWidget(SingleTestPage(self.codekey, pagedata))
                else:
                    self.questions.addWidget(PickTestPage(self.codekey, pagedata))
            self.test_name.setText(self.testname)
            self.time_limit.setTime(QtCore.QTime.fromString(self.timer))
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
            self.close()
        elif c == savebtn:
            self.savetest()
            mw.show()
            dil.hide()
            self.close()
        else:
            pass

    def savetest(self):
        global tables
        out_name = '_'.join(g for g in self.testname.split())
        if self.filename is None or self.sender() == self.save_as:
            directory = QFileDialog.getExistingDirectory()
            self.filename = directory
        else:
            directory = self.filename
        filename = directory + '\\' + out_name + '.json'
        tl = self.time_limit.time().toString()
        print(tl)
        data = {'timer': tl, 'name': self.testname, 'pages': [], 'codekey': ''}
        for i in range(1, self.questions.count()):
            self.questions.setCurrentIndex(i)
            w = self.questions.currentWidget()
            data['pages'].append(w.extractcontent())
        try:
            if directory == '':
                raise NoFileName
            if self.codekey is None:
                key = ''
                for i in range(0, 12):
                    key += str(random.randint(1, 8))
                inp = 'abcdefghijklmnopqrstuvwxyz'
                output = deencode(inp, key, False)
                while deencode(output, key, True) != inp:
                    key = ''
                    for i in range(0, 12):
                        key += str(random.randint(1, 8))
                    inp = 'abcdefghijklmnopqrstuvwxyz'
                    output = deencode(inp, key, False)
                self.codekey = key
            data['codekey'] = self.codekey
            for page in data['pages']:
                page['answer'] = deencode(page['answer'], self.codekey, False)
            with open(filename, 'w') as f:
                json.dump(data, f)
            print(data)
            if out_name not in tables:
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
            pass
        finally:
            self.refresh()


if __name__ == '__main__':
    tables = []
    app = QApplication(sys.argv)
    mw = MainWindow()
    ed = EditorWindow()
    mw.show()
    sys.exit(app.exec_())
