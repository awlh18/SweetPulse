"""
This script loads the train dataset and trains the poisson regression pipeline 
for predicting daily order volumes.

Outputs:
    - 'model/lr_pipe_orders.pkl': Trained poisson regression pipeline 

Usage:
    To be called with 'make all' command. 
"""

import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import PoissonRegressor
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline

def main():

    train_path = 'data/modelling/train.csv'
    model_path = 'model/lr_pipe_orders.pkl'

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"{train_path} does not exist")
    
    train_df = pd.read_csv(train_path, index_col=0, parse_dates=['date'])
    X_train = train_df.drop(columns=['in_store_orders'])
    y_train = train_df['in_store_orders']

    numerical_features = ['hours_opened', 'avg_temperature', 'rain', 'snow']
    categorical_features = ['is_long_weekend', 'is_HCF', 'season', 'day_of_week', 'is_holiday']
    category_orders = [
    [False, True],  # is_long_weekend
    [False, True],  # is_HCF
    ['Winter', 'Spring', 'Summer', 'Fall'],  # season
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],  # day_of_week
    [False, True]  # is_holiday
    ]
    drop_features = ['tips_normalized', 'total_sales_normalized', 'item_A_sales', 'item_B_sales', 'item_C_sales', 'HCF_sales', 'type_of_day']

    preprocessor = make_column_transformer(
    (OneHotEncoder(drop='first', categories=category_orders), categorical_features),
    (StandardScaler(), numerical_features),
    ("drop", drop_features)
    )

    pr_pipe = make_pipeline(preprocessor, PoissonRegressor())

    pr_pipe.fit(X_train, y_train)

    with open(model_path, 'wb') as f:
        pickle.dump(pr_pipe, f)
    
    print('Successfully trained pipeline for predicting daily order volumes!')

if __name__ == "__main__":
    main()