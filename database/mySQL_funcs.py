# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:12:05 2020

@author: George
"""

from mysql.connector import Error
import sqlite3
from sqlite3 import Error
import contextlib


@contextlib.contextmanager
def create_connection(db_file):
    """Create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file, isolation_level=None)
        yield connection
    except Error as e:
        raise
    finally:
        if connection:
            connection.close()


@contextlib.contextmanager
def create_cursor(db_file):
    """Creates cursor object for executing SQL queries"""
    with create_connection(db_file) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

