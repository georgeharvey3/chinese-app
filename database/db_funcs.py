# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:03:42 2020

@author: George
"""

from database.mySQL_funcs import create_cursor
import os

             
def search_by_char(char, char_set='simp'):

    """Searches word table for entry by given characters"""

    with create_cursor(file_path) as cur:
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

    """Process database entry to send to application"""

    chin, pin, mean = result
    pin_clean = pin[1:-1]
    mean_clean = tuple(mean for mean in mean.split('/') 
                       if mean and 'CL' not in mean and mean.count(' ') < 3)
    mean_clean = '/'.join(mean_clean[:3])

    return chin, pin_clean, mean_clean


def add_to_user_word(char, char_set='simp', bank=1):

    """Add an entry to the user word bank"""

    with create_cursor(file_path) as cur:
        sql = (f'''
               INSERT OR IGNORE INTO user_words (word_id, bank, date_added) VALUES (
               (SELECT id 
               FROM words
               WHERE {char_set} = "{char}"),
               {bank},
               DATE('now') 
               );
               ''')
        cur.execute(sql)


def get_user_words(char_set='simp', bank=1):

    """Return a list of all words from a given bank"""

    with create_cursor(file_path) as cur:
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

    """Moves a word from one bank to the next"""

    with create_cursor(file_path) as cur:
        sql = (f"""
               UPDATE user_words
               SET 
               bank = bank + 1,
               date_added = DATE('now')
               WHERE word_id = (SELECT id FROM words WHERE {char_set} = "{char}")""")

        cur.execute(sql)


def remove_user_word(char, char_set='simp'):

    """Remove a word from the table"""

    with create_cursor(file_path) as cur:
        sql = (f'''
               DELETE FROM user_words
               WHERE word_id = (SELECT id FROM words WHERE {char_set} = "{char}")''')
        cur.execute(sql)


def ready_counts():

    """Count how many bank 2 and bank 3 words are ready for testing"""

    with create_cursor(file_path) as cur:
        sql = (f'''
                SELECT
                COUNT(CASE
                WHEN bank = 2 AND date_added < DATE("NOW", "-7 DAY") THEN 1 END) AS bank2,
                COUNT(CASE WHEN bank = 3 AND date_added < DATE("NOW", "-1 MONTH") THEN 1 END) AS bank3
                FROM user_words;
                ''')
        cur.execute(sql)
        return cur.fetchone()


def show_table(table='user_words'):

    """Display a given table"""

    with create_cursor(file_path) as cur:
        sql = (f'''
               SELECT *
               FROM {table}
               ''')
        cur.execute(sql)
        results = cur.fetchall()

        return results


def check_for_table(table='user_words'):

    """Check that a given table exists"""

    with create_cursor(file_path) as cur:
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
        cur.execute(sql)
        result = cur.fetchall()
        return result


def create_table(name='user_words'):

    """Create a table with a given name"""

    with create_cursor(file_path) as cur:
        sql = (f"""CREATE TABLE {name} (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   word_id INTEGER UNIQUE,
                   bank INTEGER,
                   date_added DATE
                   ) 
               """)
        cur.execute(sql)


def drop_table(name):

    """Remove a table"""

    with create_cursor(file_path) as cur:
        sql = f"DROP TABLE {name}"
        cur.execute(sql)


def clear_table(name):

    """Clear a table"""

    with create_cursor(file_path) as cur:
        sql = f"DELETE FROM {name}"
        cur.execute(sql)


if __name__ == '__main__':
    file_path = "..\\data\\chinese_dict.db"
else:
    if 'chinese_repo' in os.getcwd():
        file_path = "data\\chinese_dict.db"
    else:
        file_path = os.getcwd() + "\\chinese_repo\\data\\chinese_dict.db"
