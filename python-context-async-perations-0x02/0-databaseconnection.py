import sqlite3
import traceback


class DatabaseConnection():
    def __init__(self, db):
        self.db = db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type is not None:
            print(f"""{exc_type} error:{exc_value}""")
            traceback.print_tb(exc_tb)
            return True


with DatabaseConnection('users.db') as dc:
    cursor = dc.cursor()
    cursor.execute('SELECT * FROM users;')
    results = cursor.fetchall()
    print(results[0:4])


