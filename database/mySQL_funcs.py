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
    """ create a database connection to a SQLite database """
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
    with create_connection(db_file) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()


def read_table(table):
    with create_cursor() as cur:
        sql = f'select * from {table}'
        cur.execute(sql)
        for row in cur:
            print(row)


def clear_table(table):
    with create_cursor() as cur:
        sql = f'DELETE FROM {table}'
        cur.execute(sql)


def import_from_text(text_file, table,
                     field_terminator=";", line_terminator="\n"):
    with create_cursor() as cur:
        sql = (f'''LOAD DATA 
               INFILE "{text_file}" 
               INTO TABLE {table} 
               FIELDS TERMINATED BY {field_terminator}
               LINES TERMINATED BY {line_terminator}
               IGNORE 1 LINES;
               ''')
        cur.execute(sql)


def general_query(query):
    with create_cursor() as cur:
        cur.execute(query)


def search_by_char(char, char_set='simp'):
    with create_cursor() as cur:
        sql = (f'''SELECT *
               FROM words
               WHERE {char_set} = "{char}"
               ;''')
        cur.execute(sql)
        result = cur.fetchone()

        if result:
            trad, simp, pin, mean = result
        else:
            raise ValueError('Word is not in the dictionary')
        pin_clean = pin[1:-1]
        mean_clean = tuple(mean for mean in mean.split('/')
                           if mean and 'CL' not in mean)
        clean_result = trad, simp, pin_clean, mean_clean
        return clean_result

@contextlib.contextmanager
def create_conn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        yield cur
    except Error as e:
        raise
    finally:
        if conn:
            conn.close()