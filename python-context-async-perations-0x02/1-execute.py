import sqlite3
import traceback


class ExecuteQuery():
    """context manager handling connection and query execution"""
    def __init__(self, db, query=None, *args, **kwargs):
        self.db = db
        self.conn = None
        self.cursor = None
        self.results = []
        self.query = query
        self.params = list(args)

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.executer()
        return self

    def executer(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if exc_type is not None:
            print(f"{exc_type} Exception found: {exc_value}")
            traceback.print_tb(exc_tb)
        return False


try:
    with ExecuteQuery('''users.db', "SELECT * FROM users
                        WHERE age > ?''', 25) as eq:
        print(eq.results[0:3])
except sqlite3.Error as e:
    print(f"Error found: {e}")
