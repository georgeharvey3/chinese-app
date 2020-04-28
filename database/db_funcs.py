# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:03:42 2020

@author: George
"""

from database.mySQL_funcs import connection, cursor
             
def search_by_char(char, char_set='simp'):
    with cursor() as cur:
        sql = (f'''SELECT *
               FROM words
               WHERE {char_set} = "{char}"
               ;''')
        cur.execute(sql)
        result = cur.fetchone()
        if not result:
            raise ValueError(f'{char} is not in the dictionary')
        else:
            return process_db_return(result)

def process_db_return(result, char_set='simp'):    

    trad, simp, pin, mean = result
    pin_clean = pin[1:-1]
    mean_clean = tuple(mean for mean in mean.split('/') 
                       if mean and 'CL' not in mean and mean.count(' ') < 3)
    mean_clean = '/'.join(mean_clean[:3])
    if char_set == 'simp':
        clean_result = simp, pin_clean, mean_clean 
    elif char_set == 'trad':
        clean_result = simp, pin_clean, mean_clean
    return clean_result
        
        