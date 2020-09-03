import requests
import numpy as np
import time
from datetime import datetime
#import sys
import sqlite3
from sqlite3 import Error


def create_connection(database_file):
    """ create a database connection to the SQLite database specified by database_file
    :param database_file: database file
    :return: Connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        return connection
    except Error as e:
        print(e)
    return connection

def create_table(connection, create_table):
    """ create a table from the create_table_sql statement
    :param connection: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = connection.cursor()
        c.execute(create_table)
    except Error as e:
        print(e)

def execute_command(connection, row_format, entry):
    """
    Create a new entry
    :param connection:
    :param entry:
    :return:
    """
    cur = connection.cursor()
    cur.execute(row_format, entry)
    connection.commit()

def select_all(connection, table):
    """
    Query all rows in the tasks table
    :param connection: the Connection object
    :return:
    """
    cur = connection.cursor()
    cur.execute("SELECT * FROM ?", (table,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_query(connection, query):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = connection.cursor()
    cur.execute('SELECT * FROM mempool WHERE txid=?', (query,))
    rows = cur.fetchall()
    for row in rows:
        if row:
            return True
        else:
            return None

if __name__ == '__main__':
    print('this is a module, should not be executed directly')



