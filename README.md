import sys
import mysql.connector
from PyQt6.QtWidgets import *

# ============ НАСТРОЙКИ ============
DB = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'travel'#---
}

TABLE = 'bookings'#---
USER_TABLE = 'users'
USER_ID = 'customer_id'#---
ROLES = {1: 'Администратор', 2: 'Менеджер', 3: 'Клиент'}
PROCEDURE  = 'test_procedure'
#PROCEDURE = 'get_booking_statistics'#---
# ===================================


class DB_Manager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB)

    def query(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        try:
            return cur.fetchall(), [i[0] for i in cur.description]
        except:
            return [], []

    def check_user(self, login, pwd):
        r, _ = self.query("SELECT id, role_id FROM users WHERE login=%s AND password=%s", (login, pwd))
        if r:
            return r[0][0], ROLES.get(r[0][1])
        return None, None

    def get_data(self, user_id=None):
        if user_id:
            return self.query(f"SELECT * FROM {TABLE} WHERE {USER_ID}=%s", (user_id,))
        return self.query(f"SELECT * FROM {TABLE}")

    def filter(self, col, val):
        return self.query(f"SELECT * FROM {TABLE} WHERE {col} LIKE %s", (f'%{val}%',))

    def proc(self):
        cur = self.conn.cursor()
        cur.callproc(PROCEDURE)
        return [r for result in cur.stored_results() for r in result.fetchall()]


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход в систему')
        self.setFixedSize(250, 120)

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Логин:'))
        self.login_inp = QLineEdit()
        layout.addWidget(self.login_inp)

        layout.addWidget(QLabel('Пароль:'))
        self.pwd_inp = QLineEdit()
        self.pwd_inp.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pwd_inp)

        btn = QPushButton('Войти')
        btn.clicked.connect(self.login)
        layout.addWidget(btn)

        self.login_inp.returnPressed.connect(self.login)
        self.pwd_inp.returnPressed.connect(self.login)

        self.setLayout(layout)
        self.db = None
        self.user_id = None
        self.role = None

    def login(self):
        if not self.login_inp.text() or not self.pwd_inp.text():
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля')
            return

        try:
            self.db = DB_Manager()
            self.user_id, self.role = self.db.check_user(self.login_inp.text(), self.pwd_inp.text())

            if self.user_id and self.role:
                self.accept()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка подключения:\n{e}')


class Main(QMainWindow):
    def __init__(self, db, uid, role):
        super().__init__()
        self.db, self.uid, self.role = db, uid, role
        self.setWindowTitle(f'Турагентство - {role}')#----------пом
        self.setGeometry(100, 100, 900, 500)

        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)

        layout.addWidget(QLabel(f'Роль: {role}'))

        panel = QHBoxLayout()

        if role == 'Администратор':
            self.col = QComboBox()
            self.val = QLineEdit()
            panel.addWidget(QLabel('Колонка:'))
            panel.addWidget(self.col)
            panel.addWidget(QLabel('Значение:'))
            panel.addWidget(self.val)

            btn_f = QPushButton('Фильтровать')
            btn_f.clicked.connect(self.filter)
            btn_a = QPushButton('Показать все')
            btn_a.clicked.connect(self.load)
            panel.addWidget(btn_f)
            panel.addWidget(btn_a)

        elif role == 'Менеджер':
            btn_p = QPushButton('Выполнить процедуру')
            btn_p.clicked.connect(self.proc)
            btn_r = QPushButton('Обновить')
            btn_r.clicked.connect(self.load)
            panel.addWidget(btn_p)
            panel.addWidget(btn_r)
        else:
            btn_r = QPushButton('Обновить')
            btn_r.clicked.connect(self.load)
            panel.addWidget(btn_r)

        panel.addStretch()
        layout.addLayout(panel)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load()

    def load(self):
        data, cols = self.db.get_data(self.uid if self.role == 'Клиент' else None)
        self.show_data(data, cols)
        if self.role == 'Администратор':
            self.col.clear()
            self.col.addItems(cols)

    def show_data(self, data, cols):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.resizeColumnsToContents()

    def filter(self):
        if not self.val.text():
            QMessageBox.warning(self, 'Ошибка', 'Введите значение')
            return
        data, cols = self.db.filter(self.col.currentText(), self.val.text())
        self.show_data(data, cols)

    def proc(self):
        try:
            r = self.db.proc()
            QMessageBox.information(self, 'Результат', f'Результат:\n{r}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    if login.exec() == QDialog.DialogCode.Accepted:
        w = Main(login.db, login.user_id, login.role)
        w.show()
        sys.exit(app.exec())
