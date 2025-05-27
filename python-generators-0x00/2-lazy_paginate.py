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

def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s ", (page_size_size, offset))




def lazy_paginate(page_size):
    
    page = paginate_users(page)