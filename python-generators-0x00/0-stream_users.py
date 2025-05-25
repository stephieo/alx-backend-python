#!/usr/bin/python3
import mysql.connector as msx


def connect_to_prodev():
    """connects to the ALX_prodev database
    returns:
            connection object
    """
    try:
        conn = msx.connect(user='ife', password='deputy',
                           host='localhost',
                           database='ALX_prodev')
    except msx.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)
        conn.cursor().execute('USE ALX_prodev')
        conn.cursor().close()
    return conn


def stream_users():
    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM user_data")
    for user in cur:
        yield {'user_id': user['user_id'],
               'name': user['name'],
               'email': user['email'],
               'age': int(user['age'])
        }


