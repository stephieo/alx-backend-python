import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        value = func(conn, *args, **kwargs)
        conn.close()
        return value
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) 
    return cursor.fetchone() 


#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id='c91e0ba465a148f680e144d4f27e9fc4')
print(user)