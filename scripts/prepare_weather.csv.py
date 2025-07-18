"""
This script reads the first available csv file from the `data/inputs/weather/` directory, 
extract columns required for downstream modelling, convert dates to pd.datetime, 
validates its structure and data types, and exports the result as a CSV file for downstream 
processing.

Outputs:
    - `data/processed/weather.csv`: Cleaned weather dataset for downstream use.

Usage:
    To be called with 'make all' command. 
"""

import os
import sys
import numpy as np
import pandas as pd
import glob
import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_validation import _validate_weather_df

# @click.command()
# @click.option('--weather_file', type=str, required=True, help='Excel file name')
def main():

    weather_file_list = glob.glob("data/inputs/weather/*.csv")
    destination_path = "data/processed/weather.csv"
    weather_columns = ['date','avg_temperature', 'rain', 'snow']

    if len(weather_file_list) == 0:
        raise FileNotFoundError("No weather data found in inputs/weather.")

    weather_df = pd.read_csv(weather_file_list[0])
    weather_df = weather_df[weather_columns]
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    _validate_weather_df(weather_df)

    weather_df.to_csv(destination_path, index=False)
    print("Successfully generated weather.csv!")

if __name__ == "__main__":
    main()