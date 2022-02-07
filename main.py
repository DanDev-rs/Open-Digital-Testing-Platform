import csv
import datetime
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QInputDialog, QDialog, QTableWidgetItem


tables = list()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global tables
        self.defaults = ('1-1-2021', 0)
        uic.loadUi('viewer.ui', self)
        self.bd = sqlite3.connect('results.db')
        for name in self.bd.cursor().execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall():
            tables.append(name[0])
        self.editor_btn.clicked.connect(self.editor_init)
        self.test_btn.clicked.connect(self.testing_init)
        self.btn_confirm.clicked.connect(self.filters_enable)
        self.btn_reset.clicked.connect(self.results_reset_filters)
        self.forward_btn.clicked.connect(self.next_table)
        self.back_btn.clicked.connect(self.prev_table)
        self.update_btn.clicked.connect(self.update_button)
        self.delete_btn.clicked.connect(self.confirm_delete)
        self.id = 0
        self.results_update()

    # Функции для просмотра результатов
    def results_update(self, date=None, completion=None):
        print(tables)
        self.table.setHorizontalHeaderLabels(['Номер', 'Имя', 'Дата и время', 'Результат в %'])
        if tables:
            cur = self.bd.cursor()
            table_current = tables[self.id]
            if self.id == 0:
                self.back_btn.setDisabled(True)
            else:
                self.back_btn.setDisabled(False)

            if self.id == len(tables) - 1:
                self.forward_btn.setDisabled(True)
            else:
                self.forward_btn.setDisabled(False)
            self.test_name.setText(table_current)
            self.delete_btn.setText('Удалить')
            self.delete_btn.setDisabled(False)
            self.delete_btn.clicked.connect(self.confirm_delete)
            items = cur.execute("""SELECT * FROM {}""".format(table_current)).fetchall()
            print(items)
            passed = list()
            if completion is not None and date is not None:
                for elem in items:
                    if elem[2].split()[0] == date and elem[3] >= completion:
                        passed.append(elem)
            elif completion is not None and date is None:
                for elem in items:
                    if elem[3] >= completion:
                        passed.append(elem)
            elif completion is None and date is not None:
                for elem in items:
                    if elem[2].split()[0] == date:
                        passed.append(elem)
            else:
                for elem in items:
                    print(elem)
                    passed.append(elem)

            self.table.setRowCount(len(passed))
            print(passed)
            if passed:
                for i, f in enumerate(passed):
                    for j, val in enumerate(f):
                        self.table.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.id = 0
            self.table.clear()
            self.table.setRowCount(0)
            self.test_name.clear()
            self.delete_btn.setText('Удалить')
            self.delete_btn.setDisabled(True)
            self.delete_btn.clicked.connect(self.confirm_delete)
            self.back_btn.setDisabled(True)
            self.forward_btn.setDisabled(True)

    def filters_enable(self):
        def_date, def_comp = self.defaults
        date = self.filter_date.date()
        date_filter = str(date.day()) + '-' + str(date.month()) + '-' + str(date.year())
        completion = self.filter_completion.value()
        print(date_filter, completion)
        if date_filter == def_date:
            date_filter = None
        if completion == def_comp:
            completion = None
        self.results_update(date_filter, completion)

    def results_reset_filters(self):
        self.filter_date.dateTimeFromText('01.01.2021')
        self.filter_completion.setValue(0)
        self.results_update()

    def update_button(self):
        self.results_update()

    def confirm_delete(self):
        self.delete_btn.setText('Вы уверены?')
        self.delete_btn.clicked.connect(self.delete_table)

    def delete_table(self):
        print(self.id)
        if len(tables) >= 1:
            self.bd.cursor().execute("""DROP TABLE {}""".format(tables[self.id]))
            tables.pop(self.id)
            if self.id < len(tables) - 1:
                self.id += 1
            else:
                self.id -= 1
            if len(tables) == 1:
                self.id = 0
            self.results_update()

    def next_table(self):
        if self.id < len(tables) - 1:
            self.id += 1
            self.results_update()

    def prev_table(self):
        if self.id > 0:
            self.id -= 1
            self.results_update()

    # Редактор
    def editor_init(self):
        self.editor = OpenFile()
        self.editor.show()

    # Тестировщик
    def testing_init(self):
        self.testerdialog = BeginDialog()
        self.testerdialog.show()


# Диалог открытия файла (редактор)
class OpenFile(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('editor_openfile.ui', self)
        self.cancel_btn.clicked.connect(self.cancel)
        self.open_btn.clicked.connect(self.openfile)
        self.create_btn.clicked.connect(self.check_newfile)

    def check_newfile(self):
        filename = self.inp_name.text()
        print(filename)
        if filename != '':
            exist = False
            try:
                with open(filename + '.csv', 'r', encoding='utf8') as h:
                    reader = csv.reader(h, delimiter=';', quotechar='"')
                    for i, row in enumerate(reader):
                        if row and i == 0:
                            exist = True
                        break
                if exist:
                    self.create_btn.setText('Тест с таким названием уже существует. Перезаписать?')
                    self.create_btn.clicked.connect(self.newfile)
                else:
                    self.newfile()
            except FileNotFoundError:
                self.newfile()
        else:
            self.create_btn.setText('Пожалуйста, введите название теста')

    def openfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Выбрать тест', '', 'Тест (*.csv)')[0]
        if filename != '':
            self.editor = TestEditor(filename)
            self.editor.show()
            self.hide()
        else:
            self.hide()

    def newfile(self):
        filename = self.inp_name.text()
        print(filename)
        self.editor = TestEditor(filename)
        self.editor.show()
        self.hide()

    def cancel(self):
        self.hide()


# Редактор тестов
class TestEditor(QMainWindow):
    def __init__(self, filename):
        super().__init__()
        self.content = list()
        if '.csv' not in filename:
            filename += '.csv'
            with open(filename, 'w', encoding='utf8') as f:
                writer = csv.writer(f, delimiter=';', quotechar='"')
                writer.writerow(['id', 'type', 'desc', 'options', 'answers'])
                f.close()
        with open(filename, 'r', encoding='utf8') as h:
            reader = csv.reader(h, delimiter=';', quotechar='"')
            for row in reader:
                if row:
                    self.content.append(row)
                else:
                    pass
            self.len = len(self.content)
        if self.len == 1 or self.content[1][1] not in {'single', 'multi'}:
            self.id = 0
            self.refresh_page(True)
        else:
            self.id = 1
            self.refresh_page()
        self.filename = filename

    def create_task_multi(self):
        if len(self.content) > 1:
            self.content[self.id][2] = self.desc_edit.toPlainText()
        opts = QInputDialog.getInt(self, 'Несколько ответов', 'Сколько вариантов ответа?', 2, 2, 4, 1)[0]
        self.id = len(self.content)
        if opts == 2:
            self.content.append([str(self.id), 'multi', '', '|', ''])
        elif opts == 3:
            self.content.append([str(self.id), 'multi', '', '||', ''])
        else:
            self.content.append([str(self.id), 'multi', '', '|||', ''])
        self.refresh_page()

    def create_task_single(self):
        if len(self.content) > 1:
            self.content[self.id][2] = self.desc_edit.toPlainText()
        self.id = len(self.content)
        self.content.append([str(self.id), 'single', '', '', ''])
        self.refresh_page()

    def delete_task(self):
        self.content.pop(self.id)
        if self.id - 1 == 0 and len(self.content) > 2:
            self.id += 1
            self.refresh_page()
        elif self.id - 1 > 0:
            if self.id + 1 > len(self.content) - 1:
                self.id -= 1
            else:
                self.id += 1
            self.refresh_page()
        elif len(self.content) == 2:
            self.id -= 1
            self.refresh_page(True)

    def refresh_page(self, new=False):
        if not new:
            current = self.content[self.id]
            t = current[1]
            boxtext = current[2]
            opts = current[3].split('|')
            options = len(opts)
            if t == 'single':
                uic.loadUi('editor_single.ui', self)
                self.qd_line.setText(current[3])
                self.q_line.setText(current[4])
                self.qd_line.editingFinished.connect(self.qd_edit)
                self.q_line.editingFinished.connect(self.q_edit)
            elif t == 'multi':
                if options == 2:
                    uic.loadUi('editor_multi2.ui', self)
                    if opts[0] == current[4]:
                        self.checkBox_1.setCheckState(True)
                    elif opts[1] == current[4]:
                        self.checkBox_2.setCheckState(True)
                    self.checkBox_1.stateChanged.connect(self.checked1)
                    self.checkBox_2.stateChanged.connect(self.checked2)
                elif options == 3:
                    uic.loadUi('editor_multi3.ui', self)
                    if opts[0] == current[4]:
                        self.checkBox_1.setCheckState(True)
                    elif opts[1] == current[4]:
                        self.checkBox_2.setCheckState(True)
                    elif opts[2] == current[4]:
                        self.checkBox_3.setCheckState(True)
                    self.checkBox_1.stateChanged.connect(self.checked1)
                    self.checkBox_2.stateChanged.connect(self.checked2)
                    self.checkBox_3.stateChanged.connect(self.checked3)
                    self.line3.setText(opts[2])
                    self.line3.editingFinished.connect(self.option3_edit)
                else:
                    uic.loadUi('editor_multi4.ui', self)
                    if opts[0] == current[4]:
                        self.checkBox_1.setCheckState(True)
                    elif opts[1] == current[4]:
                        self.checkBox_2.setCheckState(True)
                    elif opts[2] == current[4]:
                        self.checkBox_3.setCheckState(True)
                    elif opts[3] == current[4]:
                        self.checkBox_4.setCheckState(True)
                    self.line3.setText(opts[2])
                    self.line4.setText(opts[3])
                    self.checkBox_1.stateChanged.connect(self.checked1)
                    self.checkBox_2.stateChanged.connect(self.checked2)
                    self.checkBox_3.stateChanged.connect(self.checked3)
                    self.checkBox_4.stateChanged.connect(self.checked4)
                    self.line3.editingFinished.connect(self.option3_edit)
                    self.line4.editingFinished.connect(self.option4_edit)
                self.line1.setText(opts[0])
                self.line2.setText(opts[1])
                self.line1.editingFinished.connect(self.option1_edit)
                self.line2.editingFinished.connect(self.option2_edit)
            self.setWindowTitle('Редактор тестов - задача ' + str(self.id) + ' из ' + str(len(self.content) - 1))
            if self.id == 1:
                self.back_btn.setDisabled(True)
            else:
                self.back_btn.clicked.connect(self.task_change_left)

            if self.id + 1 <= len(self.content) - 1:
                self.forward_btn.setDisabled(False)
                self.forward_btn.clicked.connect(self.task_change_right)
            else:
                self.forward_btn.setDisabled(True)
            self.desc_edit.setPlainText(boxtext)
            self.save_action.triggered.connect(self.save_test)
            self.delete_action.triggered.connect(self.delete_task)
        else:
            uic.loadUi('editor_blank.ui', self)
        self.create_multi.triggered.connect(self.create_task_multi)
        self.create_single.triggered.connect(self.create_task_single)
        self.exit_action.triggered.connect(self.exit)

    def save_test(self):
        if len(self.content) > 1:
            self.content[self.id][2] = self.desc_edit.toPlainText()
        with open(self.filename, 'w', encoding='utf8') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"')
            for i, row in enumerate(self.content):
                if row:
                    row[0] = str(i)
                    if row[4] == '':
                        row[4] = row[3].split()[0]
                    writer.writerow(row)
            f.close()

    def reject(self):
        self.dialog.hide()

    def exit(self):
        self.dialog = SaveAcceptDialog()
        self.dialog.show()
        self.dialog.accepted.connect(self.saveexit)
        self.dialog.rejected.connect(self.reject)

    def saveexit(self):
        self.save_test()
        self.dialog.hide()
        self.close()

    def option1_edit(self):
        options = self.content[self.id][3].split('|')
        print(options)
        options[0] = self.line1.text()
        self.line1.setText(options[0])
        self.content[self.id][3] = '|'.join(g for g in options)
        print(self.content[self.id])

    def option2_edit(self):
        options = self.content[self.id][3].split('|')
        print(options)
        options[1] = self.line2.text()
        self.line2.setText(options[1])
        self.content[self.id][3] = '|'.join(g for g in options)
        print(self.content[self.id])

    def option3_edit(self):
        options = self.content[self.id][3].split('|')
        print(options)
        options[2] = self.line3.text()
        self.line3.setText(options[2])
        self.content[self.id][3] = '|'.join(g for g in options)
        print(self.content[self.id])

    def option4_edit(self):
        options = self.content[self.id][3].split('|')
        print(options)
        options[3] = self.line4.text()
        self.line4.setText(options[3])
        self.content[self.id][3] = '|'.join(g for g in options)
        print(self.content[self.id])

    def checked1(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        options = self.content[self.id][3].split('|')
        self.content[self.id][4] = options[0]
        print(self.content[self.id])
        self.refresh_page()

    def checked2(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        options = self.content[self.id][3].split('|')
        self.content[self.id][4] = options[1]
        print(self.content[self.id])
        self.refresh_page()

    def checked3(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        options = self.content[self.id][3].split('|')
        self.content[self.id][4] = options[2]
        print(self.content[self.id])
        self.refresh_page()

    def checked4(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        options = self.content[self.id][3].split('|')
        self.content[self.id][4] = options[3]
        print(self.content[self.id])
        self.refresh_page()

    def qd_edit(self):
        self.content[self.id][3] = self.qd_line.text()
        self.qd_line.setText(self.content[self.id][3])
        print(self.content[self.id])

    def q_edit(self):
        self.content[self.id][4] = self.q_line.text()
        self.q_line.setText(self.content[self.id][4])
        print(self.content[self.id])

    def task_change_left(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        if self.id - 1 > 0:
            self.id -= 1
            self.refresh_page()

    def task_change_right(self):
        self.content[self.id][2] = self.desc_edit.toPlainText()
        print(len(self.content))
        if self.id + 1 <= len(self.content) - 1:
            self.id += 1
            self.refresh_page()


class SaveAcceptDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('saveconfirmdialog.ui', self)


# Тестировщик
# Диалог открытия файла (тестировщик)
class BeginDialog(QDialog):
    def __init__(self):
        super().__init__()
        filename = QFileDialog.getOpenFileName(self, 'Выберите тест', '', 'Тест (*.csv)')[0]
        uic.loadUi('tester_start.ui', self)
        self.testcon = list()
        if filename != '':
            print(filename)
            with open(filename, 'r', encoding='utf8') as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                for row in reader:
                    if row:
                        self.testcon.append(row)
                    else:
                        pass
            self.testname = filename.split('/')[-1].split('.')[0]
            self.test_name.setText(self.testname)
            self.test_len.setText(str(len(self.testcon) - 1))
        else:
            self.begin_btn.setDisabled(True)
        if len(self.testcon) <= 1:
            self.begin_btn.setDisabled(True)
        self.begin_btn.clicked.connect(self.begin)
        self.cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        self.hide()

    def begin(self):
        username = self.lineEdit.text()
        print(username)
        self.tester = Tester(self.testcon, self.testname, username)
        self.tester.show()
        self.hide()


# Сам тестировщик
class Tester(QMainWindow):
    def __init__(self, test, testname, username):
        super().__init__()
        global tables
        self.testcontent = test
        self.testname = testname
        if username != '':
            self.username = username
        else:
            self.username = 'Ученик'
        self.answers = list()
        self.answers.append('header lol')
        for i in range(1, len(self.testcontent)):
            self.answers.append('')
        self.id = 1
        self.length = len(self.testcontent)
        self.refresh_page()

    def refresh_page(self):
        current = self.testcontent[self.id]
        t = current[1]
        boxtext = current[2]
        opts = current[3].split('|')
        options = len(opts)
        if t == 'single':
            uic.loadUi('tester_single.ui', self)
            self.q_desc.setText(current[3])
            self.q_inp.setText(self.answers[self.id])
            self.q_inp.editingFinished.connect(self.lineanswer)
        elif t == 'multi':
            if options == 2:
                uic.loadUi('tester_multi2.ui', self)
                if opts[0] == self.answers[self.id]:
                    self.checkBox_1.setCheckState(True)
                elif opts[1] == self.answers[self.id]:
                    self.checkBox_2.setCheckState(True)
                self.checkBox_1.stateChanged.connect(self.checked1)
                self.checkBox_2.stateChanged.connect(self.checked2)
            elif options == 3:
                uic.loadUi('tester_multi3.ui', self)
                self.q3.setText(opts[2])
                if opts[0] == self.answers[self.id]:
                    self.checkBox_1.setCheckState(True)
                elif opts[1] == self.answers[self.id]:
                    self.checkBox_2.setCheckState(True)
                elif opts[2] == self.answers[self.id]:
                    self.checkBox_3.setCheckState(True)
                self.checkBox_1.stateChanged.connect(self.checked1)
                self.checkBox_2.stateChanged.connect(self.checked2)
                self.checkBox_3.stateChanged.connect(self.checked3)
            else:
                uic.loadUi('tester_multi4.ui', self)
                self.q3.setText(opts[2])
                self.q4.setText(opts[3])
                if opts[0] == self.answers[self.id]:
                    self.checkBox_1.setCheckState(True)
                elif opts[1] == self.answers[self.id]:
                    self.checkBox_2.setCheckState(True)
                elif opts[2] == self.answers[self.id]:
                    self.checkBox_3.setCheckState(True)
                elif opts[3] == self.answers[self.id]:
                    self.checkBox_4.setCheckState(True)
                self.checkBox_1.stateChanged.connect(self.checked1)
                self.checkBox_2.stateChanged.connect(self.checked2)
                self.checkBox_3.stateChanged.connect(self.checked3)
                self.checkBox_4.stateChanged.connect(self.checked4)
            self.q1.setText(opts[0])
            self.q2.setText(opts[1])
        self.setWindowTitle(self.testname + ' - задача ' + str(self.id) + ' из ' + str(self.length - 1))
        if self.id == self.length - 1:
            self.forward_btn.setText('Завершить')
            self.forward_btn.clicked.connect(self.askfinish)
        else:
            self.forward_btn.clicked.connect(self.task_change_right)
        if self.id == 1:
            self.back_btn.setDisabled(True)
        else:
            self.back_btn.clicked.connect(self.task_change_left)
        self.desc_edit.setPlainText(boxtext)
        self.exit_action.triggered.connect(self.confirmexit)

    def reject(self):
        self.dialog.hide()

    def exit(self):
        self.close()

    def confirmexit(self):
        self.dialog = ExitConfirmDialog()
        self.dialog.show()
        self.dialog.accepted.connect(self.exit)
        self.dialog.rejected.connect(self.reject)

    def checked1(self):
        self.answers[self.id] = self.testcontent[self.id][3].split('|')[0]
        print(self.answers)
        self.refresh_page()

    def checked2(self):
        self.answers[self.id] = self.testcontent[self.id][3].split('|')[1]
        print(self.answers)
        self.refresh_page()

    def checked3(self):
        self.answers[self.id] = self.testcontent[self.id][3].split('|')[2]
        print(self.answers)
        self.refresh_page()

    def checked4(self):
        self.answers[self.id] = self.testcontent[self.id][3].split('|')[3]
        print(self.answers)
        self.refresh_page()

    def lineanswer(self):
        self.answers[self.id] = self.q_inp.text()
        print(self.answers)

    def task_change_left(self):
        self.testcontent[self.id][2] = self.desc_edit.toPlainText()
        if self.id - 1 > 0:
            self.id -= 1
            self.refresh_page()

    def task_change_right(self):
        self.testcontent[self.id][2] = self.desc_edit.toPlainText()
        if self.id + 1 <= len(self.testcontent) - 1:
            self.id += 1
            self.refresh_page()

    def askfinish(self):
        self.dialog = ConfirmFinishDialog()
        self.dialog.show()
        self.dialog.accepted.connect(self.finishtest)
        self.dialog.rejected.connect(self.reject)

    def finishtest(self):
        self.menubar.clear()
        uic.loadUi('tester_finish.ui', self)
        self.setWindowTitle(self.testname + ' - результат')
        correct = 0
        self.answers.pop(0)
        for i, answer in enumerate(self.answers):
            if self.testcontent[i + 1][4] == answer:
                correct += 1
        self.result.setText(str(correct) + ' из ' + str(len(self.answers)))

        bd = sqlite3.connect('results.db')
        cur = bd.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS {}(
                id INT PRIMARY KEY UNIQUE,
                name TEXT,
                date DATETIME,
                completion INT);
             """.format(self.testname))
        if self.testname not in tables:
            tables.append(self.testname)
        bd.commit()
        self.length -= 1
        completion = str(round(correct / (self.length / 100)))
        ind = cur.execute("""SELECT COUNT(*) FROM {};""".format(self.testname)).fetchone()[0] + 1
        dt = datetime.datetime.now()
        date = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year) + ' ' + str(dt.hour) + ':' + \
            str(dt.minute) + ':' + str(dt.second)
        command = """INSERT INTO {}(id,name,date,completion) VALUES({},'{}','{}',{});
        """.format(self.testname, str(ind), self.username, date, completion)
        print(command)
        cur.execute(command)
        bd.commit()
        self.exit_btn.clicked.connect(self.exit)


class ExitConfirmDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('exitconfirmdialog.ui', self)


class ConfirmFinishDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('finishconfirmdialog.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
