import os
import sys
import numpy as np
import pandas as pd
import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_validation import _validate_excel_df

@click.command()
@click.option('--excel_file', type=str, required=True, help='Excel file name')
@click.option('--sheet', type=str, required=True, help='Excel sheet name')
def main(excel_file, sheet):

    excel_root_dir = "data/inputs/sales/"
    excel_file_path = excel_root_dir + excel_file

    destination_dir = "data/processed/"
    destination_path = "data/processed/sales.csv"

    if not os.path.exists(excel_file_path):
        raise FileNotFoundError("The specificed excel file not found. Did you specify the right file?")

    excel_df = pd.read_excel(excel_file_path, sheet_name=sheet)
    
    _validate_excel_df(excel_df)

    excel_df[excel_df.select_dtypes(include='number').columns] = excel_df.select_dtypes(include='number').round(2)
    excel_df.to_csv(destination_path, index=False)
    print("Successfully generated sales.csv!")

if __name__ == "__main__":
    main()