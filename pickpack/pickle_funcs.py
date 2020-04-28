# -*- coding: utf-8 -*-
"""
pickle_funcs
"""

import os
import pickle

def read_or_new_pickle(path, default):
    '''
    Checks current directory for pickled object and returns if found
    else returns default 
    '''
    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception: # so many things could go wrong, can't be more specific.
                pass 
    with open(path, "wb") as f:
        pickle.dump(default, f)
    return default