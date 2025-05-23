import mysql.connector as msx
import uuid
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
        cursor.execute(
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
        exit(1)
        conn.cursor().execute('USE ALX_prodev')
        conn.cursor().close()
    return conn


def create_table(connection):
    """creates a table 'user_data' if not existing"""
    cursor = connection.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE user_data(
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(250) NOT NULL,
                email VARCHAR(250) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX idx_user_id (user_id)
                )'''
        )
    except msx.Error as err:
        print(" Table already exists")

    cursor.close()


def read_csv_generator(csv_file_path):
    """ a generator that reads each line of a csv file"""
    with open(csv_file_path, 'r')as f:
        datarow = csv.DictReader(f)
        for row in datarow:
            row['user_id'] = uuid.uuid4().hex

            yield {
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            }


def insert_data(connection, data):
    """inserts data in the database if non-existent using  python generator"""
    cursor = connection.cursor()
    for line in read_csv_generator(data):
        try:
            cursor.execute(
                '''INSERT INTO user_data
                (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)''',
                (line['user_id'], line['name'], line['email'], line['age'])
            )
        except msx.Error as err:
            raise err
    connection.commit()
    cursor.close()
