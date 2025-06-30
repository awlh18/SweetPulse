import os
import sys
import numpy as np
import pandas as pd
import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_validation import _validate_weather_df

@click.command()
@click.option('--weather_file', type=str, required=True, help='Excel file name')
def main(weather_file):

    weather_root_dir = "data/inputs/weather/"
    weather_file_path = weather_root_dir + weather_file

    destination_dir = "data/processed/"
    destination_path = "data/processed/weather.csv"

    weather_columns = ['date','avg_temperature', 'rain', 'snow']

    if not os.path.exists(weather_file_path):
        raise FileNotFoundError("The specificed weather file not found. Did you specify the right file?")

    weather_df = pd.read_csv(weather_file_path)
    weather_df = weather_df[weather_columns]
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    _validate_weather_df(weather_df)

    weather_df.to_csv(destination_path, index=False)
    print("Successfully generated weather.csv!")

if __name__ == "__main__":
    main()