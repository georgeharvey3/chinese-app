# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 12:57:53 2020

@author: George

"""

from datetime import datetime


def timestamp():
    
    """Obtain a timestamp"""
    
    dateTimeObj = datetime.now()
    dateString = str(datetime.date(dateTimeObj))
    
    return dateString


def days_between(d1):
    
    """Finds the number of days between two dates"""
    
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    now = datetime.strptime(timestamp(), "%Y-%m-%d")
    return abs((now - d1).days)

def date_checker(date, period):
    
    """Returns true if amount of time between date and now is greater than period"""
    
    date = date.strip()
    date = datetime.strptime(date, "%Y-%m-%d")
    now = datetime.strptime(timestamp(), "%Y-%m-%d")
    return abs((now - date).days) > period


def period_checker(file, num_days):
    
    """Searches bank to see how many entries were before a given time period"""
    
    num_hits = 0
        
    megalist = []
    if megalist:
        dates = [obj.date for obj in megalist if obj]             
        for date in dates:
            if days_between(date) >= num_days:
                num_hits += 1  

        return num_hits
    else:
        return 0


def datetime_to_str(date):
    return datetime.strftime(date, '%Y-%m-%d')