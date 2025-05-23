import sqlite3
import uuid
import csv


def setup_db():
    cnx = sqlite3.connect('users.db')
    cur = cnx.cursor()
    cur.execute(
        '''CREATE TABLE users(
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(250) NOT NULL,
            email VARCHAR(250) NOT NULL,
            age DECIMAL NOT NULL
            )'''
    )
    cnx.commit()
    cur.close()
    cnx.close()

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

def fill_db( data):
    cnx = sqlite3.connect('users.db')
    cur = cnx.cursor()
    for line in read_csv_generator(data):
        try:
            cur.execute(
                '''INSERT INTO users
                (user_id, name, email, age)
                VALUES (?, ?, ?, ?)''',
                (line['user_id'], line['name'], line['email'], line['age'])
            )
            cnx.commit()
        except sqlite3.Error as err:
            raise err
    cur.close()
    cnx.close()





if __name__ == '__main__':
    setup_db()
    cnx = sqlite3.connect('test.db')
    fill_db(cnx,'user_data.csv')