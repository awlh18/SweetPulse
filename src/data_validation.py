import pandas as pd
import pandera as pa


def _validate_excel_df(excel_df):

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime),
    "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "taiyaki_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "soft_serve_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "HCF_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)), 
    "type_of_day": pa.Column(str, pa.Check.isin(["Weekday", "Weekend", "Friday", "Unusual", "Holiday"]))
    })

    schema_features_df.validate(excel_df)

def _validate_weather_df(weather_df):

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime, nullable=True),
    "avg_temperature": pa.Column(float, nullable=True),
    "rain": pa.Column(float, nullable=True),
    "snow": pa.Column(float, nullable=True)
    })

    schema_features_df.validate(weather_df)

def _validate_combined_df(combined_df):

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime),
    "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "taiyaki_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "soft_serve_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
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
