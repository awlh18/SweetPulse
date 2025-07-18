"""
This script loads the preprocessed sales and weather data, merge them by date, engineer
features for model-training, validate data types and strcuture, drop unusual days, and peform 
train/test split. 

Outputs:
    - `data/processed/combined.csv`: Cleaned and feature-enhanced dataset.
    - `data/modelling/train.csv`: Training dataset (all but last 30 days).
    - `data/modelling/test.csv`: Test dataset (last 30 days).

Usage:
    To be called with 'make all' command. 

"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from src.data_validation import _validate_combined_df
from src.feature_functions import *

def main():

    sales_df=pd.read_csv('data/processed/sales.csv', parse_dates=['date'])
    weather_df=pd.read_csv('data/processed/weather.csv', parse_dates=['date'])

    start_date=sales_df['date'].min()
    end_date=sales_df['date'].max()

    if not start_date in weather_df['date'].values:
        return (f'Sales start date {start_date.date()} not in weather data. Please double weather data range.')
    
    if not end_date in weather_df['date'].values:
        return (f'Sales end date {end_date.date()} not in weather data. Please double check weather data range.')

    condition = weather_df['date'].between(start_date, end_date)
    weather_df = weather_df[condition]

    combined_df = pd.merge(sales_df, weather_df, on='date', how='left')

    # create features 
    combined_df['is_long_weekend']=is_long_weekend(combined_df['type_of_day'])
    combined_df['is_HCF']=is_HCF(combined_df['HCF_sales'])
    combined_df['is_holiday']=is_holiday(combined_df['type_of_day'])
    combined_df['season']=get_season(combined_df['date'])
    combined_df['day_of_week']=combined_df['date'].dt.day_name()

    # set categories
    combined_df['day_of_week'] = pd.Categorical(combined_df['day_of_week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    combined_df['season'] = pd.Categorical(combined_df['season'], categories=['Winter', 'Spring', 'Summer', 'Fall'])

    # data validation
    _validate_combined_df(combined_df)

    # drop unusual days
    unusual_days=combined_df[combined_df['type_of_day']=='Unusual'].index.to_list()
    combined_df=combined_df.drop(index=unusual_days)

    combined_df.to_csv('data/processed/combined.csv', index=False)
    print("Successfully generated combined.csv!")

    # train, test split
    train_df=combined_df.iloc[:-30]
    test_df=combined_df.iloc[-30:]
    
    train_df.to_csv('data/modelling/train.csv', index=False)
    test_df.to_csv('data/modelling/test.csv', index=False)

    print("Successfully generated train and test csv!")

if __name__ == "__main__":
    main()
