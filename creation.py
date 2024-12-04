import sqlite3


def creation():
    con = sqlite3.connect("cars2_0.sqlite")
    kursor = con.cursor()
    kursor.execute('''CREATE TABLE IF NOT EXISTS client (
                        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
                        login CHAR(50) NOT NULL,
                        name_client CHAR(50),
                        FOREIGN KEY (login) REFERENCES "users"(login)
                        );''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS "order" (
                        id_order INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_type TEXT,
                        model CHAR(50) NOT NULL,
                        status CHAR(50) NOT NULL, 
                        first_date DATE NOT NULL,
                        finish_date DATE,
                        id_worker INT,
                        final_sum INT,
                        id_client INT,
                        FOREIGN KEY (id_worker) REFERENCES worker(id_worker)
                        FOREIGN KEY (id_client) REFERENCES client(id_client)
                        );''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS "type"(
                        id_type INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_type CHAR(50) NOT NULL,
                        amount INT NOT NULL
                        );''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS worker(
                        id_worker INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_worker CHAR(50),
                        login CHAR(50) NOT NULL,
                        FOREIGN KEY (login) REFERENCES users(login)
                        );''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS administrator(
                        id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_admin CHAR(50),
                        login CHAR(50) NOT NULL,
                        FOREIGN KEY (login) REFERENCES users(login)
                        );''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        login CHAR(50) PRIMARY KEY,
                        passw CHAR(15) NOT NULL,
                        access_level INT DEFAULT 3
                        )''')

    kursor.execute('''CREATE TABLE IF NOT EXISTS type_order (
                        id INTEGER PRIMARY KEY,
                        id_type INTEGER,
                        amount INTEGER,
                        id_order INTEGER,
                        FOREIGN KEY (id_type) REFERENCES "type"(id_type),
                        FOREIGN KEY (id_order) REFERENCES "order"(id_order)
                        );''')

    con.commit()
    con.close()


def insert():
    con = sqlite3.connect("cars2_0.sqlite")
    kursor = con.cursor()

    kursor.execute('''INSERT OR REPLACE INTO users VALUES 
                    ('admin', 'admin', 1)''')

    kursor.execute('''INSERT OR REPLACE INTO type VALUES
                    (1, 'Ремонт Чайника', 5000),
                    (2, 'Ремонт Лампы', 6000)''')

    kursor.execute('''INSERT OR REPLACE INTO users VALUES
                    ('Первый', 12345, 2),
                    ('Второй', 123, 3)''')

    kursor.execute('''INSERT OR REPLACE INTO client VALUES
                    (1, 'Второй', 'ИмяВторой'),
                    (2, 'Третий', 'ИмяТретий')''')

    kursor.execute('''INSERT OR REPLACE INTO worker VALUES
                    (1, 'ИмяПервый', 'Первый')''')

    kursor.execute('''INSERT OR REPLACE INTO "order"(id_order, id_type, model, status, first_date, finish_date, id_worker, id_client, final_sum) VALUES
                    (1, NULL, 'Чайник "ОТ БАБУШКИ"', 'ГОТОВ', 'q', 'q', 1, 1, 0),
                    (2, NULL, 'Лампа 100500', 'ГОТОВ', 'q', 'q', 2, 2, 0)''')

    kursor.execute('''INSERT OR REPLACE INTO type_order VALUES
                    (1, 1, 2, 2),
                    (2, 2, 3, 1),
                    (3, 2, 3, 1)''')

    con.commit()
    con.close()


if __name__ == '__main__':
    insert()

