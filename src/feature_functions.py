# Core libraries
import numpy as np
import pandas as pd
import os
import sys

def get_season(dates: pd.Series) -> pd.Series:
    """
    Given a Series of datetime objects, return a Series with the season for each date.
    Seasons are based on meteorological seasons in the Northern Hemisphere.
    """
    def season_of_date(date):
        month = date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    if isinstance(dates, pd.Series):
        return dates.apply(season_of_date).rename("season")
    else:
        return season_of_date(dates)

def is_HCF(HCF_sales):

    HCF_days = HCF_sales > 0
    HCF_days.name = 'is_HCF'

    return HCF_days

def is_holiday(dates):

    holidays = dates.apply(lambda day: day == 'Holiday')

    return holidays

def is_long_weekend(type_of_days):

    is_long_weekend_list = [False] * len(type_of_days)

    for i ,day in enumerate(type_of_days):

        if day == 'Holiday':
            prev_day = type_of_days[i-1] if i > 0 else None
            next_day = type_of_days[i+1] if i < len(type_of_days) - 1 else None 
            
            if prev_day == 'Weekend':
                is_long_weekend_list[i] = True
                is_long_weekend_list[i-1] = True
                is_long_weekend_list[i-2] = True
            
            if next_day == 'Weekend':
                is_long_weekend_list[i] = True
                is_long_weekend_list[i+1] = True
                is_long_weekend_list[i+2] = True
    
    return pd.Series(is_long_weekend_list, name='is_long_weekend')