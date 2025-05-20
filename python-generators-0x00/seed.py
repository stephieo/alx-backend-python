# from sqlalchemy import create_engine, Column, String, 
# from sqlalchemy.dialects.mysql import UUID
# from sqlalchemy.orm import declarative_base, sessionmaker
import mysql.connector as msx
import csv

def connect_db():
    """ connects  to a a myssql databases server
    returns:
            connection object
    """
    try:
        conn = msx.connect(user='ife', password='deputy',
                           host='localhost')
    except msx.Error as err:
        print("Error connecting to server")

    return conn    

def create_database(connection):
    """ creates the ALX_prodev database"""
    cursor = connection.cursor()
    try:
        connection.execute(
            "CREATE DATABASE ALX_prodev"
        )
    except msx.Error as err:
        print(" Database already exists")

    cursor.close()
    connection.close()
   
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
        print("Error connecting to database")

    return conn 

def create_table(connection):
    """creates a table 'user_data' if not existing"""
    cursor = connection.cursor()
    try:
        connection.execute(
            '''CREATE TABLE user_data(
                user_id UUID PRIMARY KEY,
                name VARCHAR(250) NOT NULL,
                email VARCHAR(250) NOT NULL,
                age DECIMAL NOT NULL
                Index idx_user_id (user_id)
                )'''
        )
    except msx.Error as err:
        print(" Table already exists")

    cursor.close()
    connection.close()
    
def read_csv_generator(csv_file_path):
    """ a generator that reads each line of a csv file"""
    with open(csv_file_path, 'r')as f:
        for line in f:
            yield line.strip()

def insert_data(connection, data):
    """inserts data in the database if non-existent using  python generator"""
    cursor = connection.cursor()
    print(next(read_csv_generator(data)))

        


connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')