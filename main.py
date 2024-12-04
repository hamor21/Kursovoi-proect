import sys
import sqlite3
import creation
from random import randint
from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelation, QSqlRelationalTableModel
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QDialog
)

Name = ''
LEVEL = 3


class Table(QWidget):
    def __init__(self, vidget_name: str, table_name, line: list):
        super().__init__()
        createConnection()
        self.setWindowTitle(f"{vidget_name}")
        self.resize(700, 700)
        # Set up the model
        db = QSqlDatabase.database('CARS')
        self.model = QSqlTableModel(self, db)
        self.model.setTable(f"{table_name}")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        for i in range(len(line)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, line[i])
        # self.model.setHeaderData(0, Qt.Orientation.Horizontal, "Индивидуальный номер услуги")
        # self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Название услуги")
        # self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Цена услуги")
        # self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Email")
        self.model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setWindowTitle(f"{vidget_name}")
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.show()


class Login(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.enter_button.clicked.connect(self.check_user)
        self.registration_button.clicked.connect(self.registration)

    def check_user(self):
        try:
            if self.password_line.text() == ask('passw', 'users', self.login_line.text()):
                global LEVEL, Name
                Name = self.login_line.text()
                LEVEL = int(ask('access_level', 'users', self.login_line.text()))
                self.accept()
            else:
                self.item = QMessageBox()
                self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
                self.item.show()
        except IndexError:
            self.item = QMessageBox()
            self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
            self.item.show()

    def registration(self):
        insert(['', 'users', 'login', 'passw', 'ФИО'], True)


class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search = []
        self.view = None
        self.aut = Login()
        self.aut.show()
        if self.aut.exec():
            self.setupUI()

    def table_connect(self):
        global LEVEL
        createConnection()
        db = QSqlDatabase.database('CARS')
        model = QSqlRelationalTableModel(self, db)
        model.setTable(f"{self.search[1]}")
        # model.qu
        if LEVEL == 1:
            model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        for i in range(len(self.search[2:])):
            model.setHeaderData(i, Qt.Orientation.Horizontal, self.search[2:][i])
        if self.search[1] == '"order"':
            model.setRelation(8, QSqlRelation("client", "id_client", "name_client"))
        model.select()
        if LEVEL == 3 and self.search[1] == '"order"':
            search = ask('id_client', 'client', Name)
            model.setFilter(f'"order".id_client = {search}')
        elif LEVEL == 2 and self.search[1] == '"order"':
            search = ask('id_worker', 'worker', Name)
            model.setFilter(f'"order".id_worker = {search}')
        model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setWindowTitle(f"{self.search[0]}")
        self.view.setModel(model)
        self.view.resizeColumnsToContents()
        self.view.show()

    def type_but(self):
        self.search = []
        self.search.append('Услуги')
        self.search.append('type')
        self.search.append("Индивидуальный номер услуги")
        self.search.append('Название услуги')
        self.search.append('Цена услуги')
        self.table_connect()

    def worker_but(self):
        self.search = []
        self.search.append('Работники')
        self.search.append('worker')
        self.search.append('ID работника')
        self.search.append('ФИО')
        self.search.append('Заказ в работе')
        self.search.append('Предыдущие заказы')
        self.search.append('Логин')
        self.table_connect()

    def order_but(self):
        #creation.summa()
        self.search = []
        self.search.append('Заказы')
        self.search.append('"order"')
        self.search.append('Номер заказа')
        self.search.append('Необходимые услуги')
        self.search.append('Модель изделия') ########################
        self.search.append('Сатус')
        self.search.append('Дата начала работ')
        self.search.append('Дата окончания работ')
        self.search.append('Ответственный работник')
        self.search.append('Итоговая сумма')
        self.search.append('Номер клиента')
        summa()
        self.table_connect()

    def client_but(self):
        self.search = []
        self.search.append('Клиенты')
        self.search.append('client')
        self.search.append('ID клиента')
        self.search.append('Имя клиента')
        self.search.append('Прошлые заказы')
        self.table_connect()

    def inf_but(self):
        self.search = []
        self.search.append('Информация')
        self.search.append('worker')
        self.search.append('ID работника')
        self.search.append('ФИО')
        self.search.append('Заказ в работе')
        self.search.append('Предыдущие заказы')
        self.search.append('Логин')
        self.table_connect()

    def order_new(self):
        self.search = []
        self.search.append('Заказы')
        self.search.append('"order"')
        self.search.append('Необходимые услуги')
        self.search.append('Модель изделия')
        self.search.append('Дата начала работ')
        self.search.append('Ответственный работник')
        self.search.append('Номер клиента')
        result = insert(self.search)
        name = ''
        amount = 0
        con = sqlite3.connect('cars2_0.sqlite')
        kursor = con.cursor()
        if result:
            for i in result[0].split(';'):
                if i == '':
                    continue
                i = i.split('-')
                name = str(i[0])
                amount = int(i[1])
                search_id = kursor.execute('''SELECT id_type FROM "type" WHERE name_type = ?''', (name, )).fetchall()[0][0]
                search_id_2 = kursor.execute('''select count(*) from "order"''').fetchall()[0][0] + 1
                k = () + (search_id, )
                k += (amount, ) + (search_id_2, )
                kursor.execute(f'''INSERT INTO type_order (id_type, amount, id_order) VALUES
                                    (?, ?, ?);''', k)
                con.commit()
            kursor.execute(f'''INSERT INTO "order"(status, id_type, model, first_date, id_worker, id_client, final_sum) VALUES
                            ('НЕ ГОТОВ', ?, ?, ?, ?, ?, 0)''', tuple(result))
            con.commit()
            con.close()

    def type_new(self):
        self.search = []
        self.search.append('Услуги')
        self.search.append('type')
        self.search.append('Название услуги')
        self.search.append('Цена услуги')
        insert(self.search)

    def worker_new(self):
        self.search = []
        self.search.append('Работники')
        self.search.append('worker')
        self.search.append('ФИО')
        self.search.append('Логин')
        insert(self.search, add=True)

    def client_new(self):
        self.search = []
        self.search.append('Клиенты')
        self.search.append('client')
        self.search.append('Имя заказа')
        self.search.append('Прошлые заказы')
        insert(self.search, add=True)

    def setupUI(self):
        uic.loadUi('admin.ui', self)
        if LEVEL == 1:
            self.type_button.clicked.connect(self.type_but)
            self.order_button.clicked.connect(self.order_but)
            self.worker_button.clicked.connect(self.worker_but)
            self.client_button.clicked.connect(self.client_but)
            self.new_order.clicked.connect(self.order_new)
            self.new_worker.clicked.connect(self.worker_new)
            self.new_type.clicked.connect(self.type_new)
        if LEVEL == 2:
            self.type_button.clicked.connect(self.type_but)
            self.order_button.clicked.connect(self.order_but)
            self.client_button.hide()
            self.worker_button.hide()
            self.new_order.hide()
            self.new_worker.hide()
            self.new_type.hide()
        if LEVEL == 3:
            self.worker_button.hide()
            self.type_button.hide()
            self.client_button.hide()
            self.new_type.hide()
            self.new_order.hide()
            self.new_worker.hide()
            self.order_button.clicked.connect(self.order_but)


def insert(search: list, reg=False, add=False, who='worker'):
    line = []
    for i in search[2:]:
        item = QDialog()
        item.setWindowTitle(i)
        layout = QVBoxLayout()
        message = QLineEdit()
        ok_but = QPushButton()
        cancel = QPushButton()
        layout.addWidget(message)
        layout.addWidget(ok_but)
        layout.addWidget(cancel)
        item.setLayout(layout)
        ok_but.clicked.connect(item.accept)
        cancel.clicked.connect(item.reject)
        ok_but.setText('OK')
        cancel.setText('ОТМЕНА')
        item.show()
        if item.exec():
            line.append(message.text())
        else:
            return None
    if search[1] == '"order"':
        return line
    con = sqlite3.connect("cars2_0.sqlite")
    kursor = con.cursor()

    k = ', '
    kursor.execute(f'PRAGMA table_info({search[1]})')
    column_names = [i[1] for i in kursor.fetchall()]
    if reg:
        line.append(3)
        line = tuple(line)
        print(line)
        kursor.execute(f'''INSERT OR REPLACE INTO client(login, name_client) VALUES
                                            ({'?, ?'});''', (line[0], line[-1]))
        kursor.execute(f'''INSERT OR REPLACE INTO {search[1]} ({k.join(column_names)}) VALUES
                                (?, ?, ?);''', (line[0], line[1], line[-1]))
    else:
        line = tuple(line)
        kursor.execute(f'''INSERT OR REPLACE INTO {search[1]} ({k.join(column_names[1:])}) VALUES
                                        ({'?, ' * (len(column_names[1:]) - 1) + '?'});''', line)
    if add:
        kursor.execute(
            f'''INSERT INTO users (login, passw, access_level)
                VALUES (?, ?, ?)''', (f"{who + str(randint(1, 5))}", '111', f"{2 if who == 'worker' else 3}"))
    con.commit()
    con.close()


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE", 'CARS')
    con.setDatabaseName("cars2_0.sqlite")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


def ask(column: str, table: str, uslovie: str):
    con = sqlite3.connect('cars2_0.sqlite')
    kur = con.cursor()
    line_1 = kur.execute(f"""SELECT {column} FROM {table} WHERE login = ?""", (uslovie,)).fetchall()[0]
    con.close()
    return str(line_1[0])


def summa():
    answer = []
    con = sqlite3.connect("cars2_0.sqlite")
    kursor = con.cursor()

    line = kursor.execute('''SELECT "order".id_order, type_order.amount, "type".name_type, "type".amount FROM "order"
                                INNER JOIN type_order ON "order".id_order = type_order.id_order
                                INNER JOIN "type" ON "type".id_type = type_order.id_type;''').fetchall()
    kursor.execute(f'''UPDATE "order" SET final_sum = 0,
                                            id_type = NULL''')
    con.commit()
    for i in line:
        current_value = kursor.execute(f'''SELECT id_type FROM "order" WHERE id_order = {i[0]}''').fetchall()[0][0]
        new_value = f"{i[2] + '-' + str(i[1]) + ';'}"
        if not current_value:
            kursor.execute(f'''UPDATE "order"
                                        SET id_type = "{new_value}"
                                        WHERE id_order = {i[0]};''')
        else:
            kursor.execute(f'''UPDATE "order"
                            SET id_type = "{current_value + new_value}"
                            WHERE id_order = {i[0]};''')
        con.commit()
        current_value = kursor.execute(f'''SELECT final_sum FROM "order" WHERE id_order = {i[0]}''').fetchall()[0][0]
        new_value = f"{i[1] * i[-1]}"
        if not current_value:
            kursor.execute(f'''UPDATE "order"
                                        SET final_sum = {int(new_value)}
                                        WHERE id_order = {i[0]};''')
        else:
            kursor.execute(f'''UPDATE "order"
                            SET final_sum = {int(current_value) + int(new_value)}
                            WHERE id_order = {i[0]};''')
        con.commit()
    con.close()


if __name__ == '__main__':
    creation.creation()
    creation.insert()
    app = QApplication(sys.argv)
    new = Admin()
    new.show()
    sys.exit(app.exec())
