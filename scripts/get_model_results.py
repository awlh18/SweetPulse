import os
import sys
import numpy as np
import pandas as pd
import pickle
import click
from sklearn.metrics import mean_squared_error, mean_absolute_error

def main():

    test_path = 'data/modelling/test.csv'
    model_path = 'model/lr_pipe_total_sales.pkl'
    coef_df_path = 'results/trained_coef_total_sales.csv'
    mae_grouped_df_path = 'results/mae_grouped_total_sales.csv'

    if not os.path.exists(test_path):
        raise FileNotFoundError(f"{test_path} does not exist")

    test_df = pd.read_csv(test_path)
    X_test = test_df.drop(columns=['total_sales_normalized'])
    y_test = test_df['total_sales_normalized']

    with open(model_path, 'rb') as f:
        lr_pipe = pickle.load(f)

    columns = (lr_pipe.named_steps['columntransformer']['onehotencoder'].get_feature_names_out().tolist() + 
           lr_pipe.named_steps['columntransformer']['standardscaler'].get_feature_names_out().tolist())
    coef = lr_pipe.named_steps['linearregression'].coef_

    coef_df = pd.DataFrame({
        'features': columns,
        'coefficients': coef
    })

    coef_df = coef_df.sort_values(by='coefficients', ascending=False).reset_index(drop=True).round(0)
    coef_df.to_csv(coef_df_path, index=False)

    y_pred = lr_pipe.predict(X_test)

    pred_results = test_df.copy()
    pred_results['y_pred'] = y_pred
    pred_results['prediction_error'] = pred_results['y_pred'] - pred_results['total_sales_normalized'] 

    mae_grouped_df = pred_results.groupby('day_of_week')[['total_sales_normalized', 'y_pred', 'prediction_error']].mean().round(2)
    mae_grouped_df['error_percentage'] = ((abs(mae_grouped_df['prediction_error']) / mae_grouped_df['total_sales_normalized'])*100).round(2)

    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mae_grouped_df =  mae_grouped_df.loc[weekday_order]

    mae_grouped_df.to_csv(mae_grouped_df_path, index=False)

    print("Successfully generated results for total sales prediction!")

if __name__ == "__main__":
    main()


