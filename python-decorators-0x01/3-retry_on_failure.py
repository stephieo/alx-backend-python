import time
import sqlite3
import functools
import time


def with_db_connection(func):
    @functools.wraps(func)
    def db_wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        value = func(conn, *args, **kwargs)
        conn.close()
        return value
    return db_wrapper


def retry_on_failure(retries, delay):
    def retry_decorator(func):
        @functools.wraps(func)
        def retry_wrapper(*args, **kwargs):
            exec_counter = 0
            while exec_counter <= retries:
                try:
                    value = func(*args, **kwargs)
                    break
                except sqlite3.Error as e:
                    exec_counter += 1
                    if exec_counter <= retries:
                        time.sleep(delay)
                        print("retrying....")
                    else:
                        raise e
            return value
        return retry_wrapper
    return retry_decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
