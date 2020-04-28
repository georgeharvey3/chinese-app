# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:12:05 2020

@author: George
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:03:42 2020

@author: George
"""

import database.db_config as db_config
import mysql.connector
from mysql.connector import Error
import contextlib


@contextlib.contextmanager
def connection(host=db_config.HOST, user=db_config.USER,
               passwd=db_config.PASS, dbname=db_config.MYDB):
    connection = mysql.connector.connect(
            host=host, user=user, passwd=passwd, db=dbname)
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

@contextlib.contextmanager
def cursor(host=db_config.HOST, user=db_config.USER,
           passwd=db_config.PASS, dbname=db_config.MYDB):
    with connection(host, user, passwd, dbname) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

def read_table(table):
    with cursor() as cur:
        sql = f'select * from {table}'
        cur.execute(sql)
        for row in cur:
            print(row)
            
def clear_table(table):
    with cursor() as cur:
        sql = f'DELETE FROM {table}'
        cur.execute(sql)
        

def import_from_text(text_file, table, 
                     field_terminator=";", line_terminator = "\n"):
    with cursor() as cur:
        sql = (f'''LOAD DATA 
               INFILE "{text_file}" 
               INTO TABLE {table} 
               FIELDS TERMINATED BY {field_terminator}
               LINES TERMINATED BY {line_terminator}
               IGNORE 1 LINES;
               ''')
        cur.execute(sql)     
        
def general_query(query):
    with cursor() as cur:
        cur.execute(query)
             
def search_by_char(char, char_set='simp'):
    with cursor() as cur:
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
            
        
        