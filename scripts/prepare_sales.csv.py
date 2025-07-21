"""
This script reads the first available Excel file from the `data/inputs/sales/` directory, 
validates its structure and data types, rounds numeric columns to two decimal places, 
and exports the result as a CSV file for downstream processing.

Outputs:
    - `data/processed/sales.csv`: Cleaned sales dataset for downstream use.

Usage:
    To be called with 'make all' command. 
"""

import os
import sys
import numpy as np
import pandas as pd
import glob
#import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_validation import _validate_excel_df

# @click.command()
# @click.option('--excel_file', type=str, required=True, help='Excel file name')
# @click.option('--sheet', type=str, required=True, help='Excel sheet name')
def main():

    excel_file_list = glob.glob("data/inputs/sales/*.xlsx")
    destination_path = "data/processed/sales.csv"

    if len(excel_file_list) == 0:
        raise FileNotFoundError("No sales data found in inputs/sales.")

    excel_df = pd.read_excel(excel_file_list[0], sheet_name='inputs')
    
    _validate_excel_df(excel_df)

    excel_df[excel_df.select_dtypes(include='number').columns] = excel_df.select_dtypes(include='number').round(2)
    excel_df.to_csv(destination_path, index=False)
    print("Successfully generated sales.csv!")

if __name__ == "__main__":
    main()