import time
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


query_cache = {}


def cache_query(func):
    @functools.wraps(func)
    def cache_wrapper(*args, **kwargs):
        # if query is new, save to dictionary, keys will the query
        # values will be the result
        # check if query is  a key in dict , if yes , return the  vakue
        # if no, cache and then return value
        query = args[0]
        if query not in query_cache.keys():
            result = func(*args, **kwargs)
            query_cache[query] = result
        return query_cache[query]
    return cache_wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users[0:4])

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again[0:4])
