import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline

def main():
    train_path = 'data/modelling/train.csv'
    model_path = 'model/lr_pipe_total_sales.pkl'

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"{train_path} does not exist")
    
    train_df = pd.read_csv(train_path, index_col=0, parse_dates=['date'])
    X_train = train_df.drop(columns=['total_sales_normalized'])
    y_train = train_df['total_sales_normalized']

    numerical_features = ['hours_opened', 'avg_temperature', 'rain', 'snow']
    categorical_features = ['is_long_weekend', 'is_HCF', 'season', 'day_of_week', 'is_holiday']
    category_orders = [
    [False, True],  # is_long_weekend
    [False, True],  # is_HCF
    ['Winter', 'Spring', 'Summer', 'Fall'],  # season
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],  # day_of_week
    [False, True]  # is_holiday
    ]
    drop_features = ['tips_normalized', 'in_store_orders', 'taiyaki_sales', 'soft_serve_sales', 'drink_sales', 'HCF_sales', 'type_of_day']

    preprocessor = make_column_transformer(
    (OneHotEncoder(drop='first', categories=category_orders), categorical_features),
    (StandardScaler(), numerical_features),
    ("drop", drop_features)
    )

    lr_pipe = make_pipeline(preprocessor, LinearRegression())

    lr_pipe.fit(X_train, y_train)

    with open(model_path, 'wb') as f:
        pickle.dump(lr_pipe, f)
    
    print('Successfully trained pipeline for predicting total sales!')

if __name__ == "__main__":
    main()