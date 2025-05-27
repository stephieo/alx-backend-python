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

#TODO: i'm not satisfied, multiple calls should not start streaming from the beginning
def stream_users_in_batches(batch_size):
    offset = 0
    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)
    while True:
        cur.execute("SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s ", (batch_size, offset))
        if cur.rowcount == 0:
            break
        for user in cur:
            yield {'user_id': user['user_id'],
                'name': user['name'],
                'email': user['email'],
                'age': int(user['age'])
            }
        offset += batch_size


def batch_processing(batch_size):
    batch_results = stream_users_in_batches(batch_size)
    for result in batch_results:
        if result['age'] > 25:
            print(result)
        



