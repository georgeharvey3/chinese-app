# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:03:42 2020

@author: George
"""

from database.mySQL_funcs import connection, cursor

             
def search_by_char(char, char_set='simp'):
    with cursor() as cur:
        sql = (f'''
               SELECT 
               {char_set},
               pinyin,
               meaning 
               FROM words
               WHERE {char_set} = "{char}"
               ;''')
        cur.execute(sql)
        result = cur.fetchone()
        if not result:
            raise ValueError(f'{char} is not in the dictionary')
        else:
            return process_db_return(result)


def process_db_return(result):


    chin, pin, mean = result
    pin_clean = pin[1:-1]
    mean_clean = tuple(mean for mean in mean.split('/') 
                       if mean and 'CL' not in mean and mean.count(' ') < 3)
    mean_clean = '/'.join(mean_clean[:3])

    return chin, pin_clean, mean_clean


def add_to_user_word(char, char_set='simp', bank=1):
    with cursor() as cur:
        sql = (f'''
               INSERT IGNORE INTO user_words (word_id, bank, date_added) VALUES (
               (SELECT id 
               FROM words
               WHERE {char_set} = "{char}"),
               {bank},
               CURDATE() 
               );
               ''')
        cur.execute(sql)


def get_user_words(char_set='simp', bank=1):
    with cursor() as cur:
        sql = (f'''
               SELECT
               {char_set},
               pinyin, 
               meaning
               FROM words w
               JOIN user_words uw
               ON w.id = uw.word_id 
               WHERE bank = {bank} 
               ''')
        cur.execute(sql)
        results = cur.fetchall()
        processed = [process_db_return(result) for result in results]

        return processed

def change_user_word_bank(char, char_set='simp'):
    with cursor() as cur:
        sql = (f'''
               UPDATE user_words
               SET 
               bank = bank + 1,
               date_added = CURDATE()
               WHERE word_id = (SELECT id FROM words WHERE {char_set} = "{char}")''')

        cur.execute(sql)

def remove_user_word(char, char_set='simp'):
    with cursor() as cur:
        sql = (f'''
               DELETE FROM user_words
               WHERE word_id = (SELECT id FROM words WHERE {char_set} = "{char}")''')
        cur.execute(sql)

def ready_counts():
    with cursor() as cur:
        sql = (f'''
        SELECT
        COUNT(CASE
        WHEN bank = 2 AND date_added < DATE_SUB(CURDATE(), INTERVAL 7 DAY) THEN 1 END) AS bank2,
        COUNT(CASE WHEN bank = 3 AND date_added < DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN 1 END) AS bank3
        FROM user_words;
        ''')
        cur.execute(sql)
        return cur.fetchone()

def show_table(table='user_words'):
    with cursor() as cur:
        sql = (f'''
               SELECT *
               FROM {table}
               ''')
        cur.execute(sql)
        results = cur.fetchall()

        return results

