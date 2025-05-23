import sqlite3
import functools
import logging
from os import sys
from datetime import datetime


# decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # setting up logger
        # create custom logger
        logger = logging.getLogger(__name__)
        logger.setLevel("DEBUG")
        # create handler and add to logger
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        # create formatter and add to handler
        formatter = logging.Formatter(
            '{levelname} - {message}',
            style='{',
        )
        console_handler.setFormatter(formatter)
        logger.debug(f"{datetime.now()} - Using query: {kwargs['query']}")
        value = func(*args, **kwargs)
        return value
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users[0:4])
