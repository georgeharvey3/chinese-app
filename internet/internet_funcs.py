# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:31:30 2020

@author: George
"""

import urllib.request as url
import urllib.error as urle

def internet_on():
    
    '''
    Test internet connection
    '''
    
    try:
        url.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urle.URLError: 
        return False
