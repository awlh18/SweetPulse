import pandas as pd
import pandera as pa


def _validate_excel_df(excel_df):
    """
    Validate the structure and data types of excel_df.
    To be used with `scripts/prepare_sales.csv.py`.

    Parameters
    ----------
    excel_df: pd.DataFrame
        The DataFrame (excel_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime),
    "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_A_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_B_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_C_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "HCF_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)), 
    "type_of_day": pa.Column(str, pa.Check.isin(["Weekday", "Weekend", "Friday", "Unusual", "Holiday"]))
    })

    schema_features_df.validate(excel_df)

def _validate_weather_df(weather_df):
    """
    Validate the structure and data types of weather_df.
    To be used with `scripts/prepare_weather.csv.py`.

    Parameters
    ----------
    weather_df: pd.DataFrame
        The DataFrame (weather_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime, nullable=True),
    "avg_temperature": pa.Column(float, nullable=True),
    "rain": pa.Column(float, nullable=True),
    "snow": pa.Column(float, nullable=True)
    })

    schema_features_df.validate(weather_df)

def _validate_combined_df(combined_df):
    """
    Validate the structure and data types of combined_df.
    To be used with `scripts/prepare_combined.csv.py`.

    Parameters
    ----------
    combined_df: pd.DataFrame
        The DataFrame (combined_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime),
    "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_A_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_B_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "item_C_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "HCF_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)), 
    "type_of_day": pa.Column(str, pa.Check.isin(["Weekday", "Weekend", "Friday", "Unusual", "Holiday"])),
    "avg_temperature": pa.Column(float, nullable=True),
    "rain": pa.Column(float, nullable=True),
    "snow": pa.Column(float, nullable=True),
    "is_long_weekend":pa.Column(bool),
    "is_HCF": pa.Column(bool),
    "is_holiday": pa.Column(bool),
    "day_of_week": pa.Column(pa.Category, pa.Check.isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])),
    "season": pa.Column(pa.Category, pa.Check.isin(['Winter', 'Spring', 'Summer', 'Fall']))
    })

    schema_features_df.validate(combined_df)
