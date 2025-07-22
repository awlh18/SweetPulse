"""
This script loads the preprocessed training and test datasets, and the trained
Poisson Regression model pipeline for order volumes. It evaluates model performance, extracts feature
coefficients, computes prediction errors, and generates graph to assess model fit.

Outputs:
    - `results/trained_coef_orders.csv`: Sorted list of model coefficients.
    - `results/mae_grouped_orders.csv`: MAE and error percentage by day of week.
    - `results/pr_plot_orders.pkl`: Plotly figure showing model predictions vs. actuals.
    - `results/resid_fit_plot_orders.pkl`: Residuals vs. fitted values plot.
    - `results/resid_dist_plot_orders.pkl`: Distribution of residuals.

Usage:
    To be called with 'make all' command. 

"""

import os
import sys
import numpy as np
import pandas as pd
import pickle
import click
import plotly.express as px
from sklearn.metrics import mean_squared_error, mean_absolute_error

def main():

    train_df_path = 'data/modelling/train.csv'
    test_df_path = 'data/modelling/test.csv'
    model_path = 'model/pr_pipe_orders.pkl'
    coef_df_path = 'results/trained_coef_orders.csv'
    mae_grouped_df_path = 'results/mae_grouped_orders.csv'
    pr_plot_path = 'results/pr_plot_orders.pkl'
    resid_fit_plot_path = 'results/resid_fit_plot_orders.pkl'
    resid_dist_plot_path = 'results/resid_dist_plot_orders.pkl'

    if not os.path.exists(train_df_path):
        raise FileNotFoundError(f"{train_df_path} does not exist")

    if not os.path.exists(test_df_path):
        raise FileNotFoundError(f"{test_df_path} does not exist")

    # reading in data 
    train_df = pd.read_csv(train_df_path, index_col=0, parse_dates=True)
    test_df = pd.read_csv(test_df_path, index_col=0, parse_dates=True)

    X_train = train_df.drop(columns=['in_store_orders'])
    y_train = train_df['in_store_orders']

    X_test = test_df.drop(columns=['in_store_orders'])
    y_test = test_df['in_store_orders']

    # load trained model
    with open(model_path, 'rb') as f:
        pr_pipe = pickle.load(f)

    # prepare coefficient df
    columns = (pr_pipe.named_steps['columntransformer']['onehotencoder'].get_feature_names_out().tolist() + 
           pr_pipe.named_steps['columntransformer']['standardscaler'].get_feature_names_out().tolist())
    coef = pr_pipe.named_steps['poissonregressor'].coef_
    coef = np.exp(coef)

    coef_df = pd.DataFrame({
        'features': columns,
        'coefficients': coef
    })

    coef_df = coef_df.sort_values(by='coefficients', ascending=False).reset_index(drop=True).round(2)
    coef_df.to_csv(coef_df_path, index=False)

    # prepare MAE by day of the week df 
    y_pred = pr_pipe.predict(X_test)

    pred_results = test_df.copy()
    pred_results['y_pred'] = y_pred
    pred_results['prediction_error'] = pred_results['y_pred'] - pred_results['in_store_orders'] 

    mae_grouped_df = pred_results.groupby('day_of_week')[['in_store_orders', 'y_pred', 'prediction_error']].mean().round(2)
    mae_grouped_df['error_percentage'] = (mae_grouped_df['prediction_error'] / mae_grouped_df['in_store_orders']).round(3)

    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mae_grouped_df =  mae_grouped_df.loc[weekday_order]

    mae_grouped_df.to_csv(mae_grouped_df_path)

    # prepare prediction vs actual graph 
    y_train_pred = pr_pipe.predict(X_train)
    y_train_for_plot = pd.DataFrame(y_train).assign(label='train')
    y_test_for_plot = pd.DataFrame(y_test).assign(label='test')
    pr_pred_for_plot = pd.DataFrame(y_pred, columns=['in_store_orders'], index=y_test.index).assign(label='test_prediction')
    y_train_pred_for_plot = pd.DataFrame(y_train_pred, columns=['in_store_orders'], index=y_train.index).assign(label='train_prediction')

    custom_colors = {
    'train': '#1f77b4',
    'test': '#d62728',
    'test_prediction': '#8bc34a',
    'train_prediction': '#4caf50'
    }

    pr_plot_fig = px.line(pd.concat((y_train_for_plot, y_test_for_plot, y_train_pred_for_plot, pr_pred_for_plot)), 
        y="in_store_orders",
        color='label', 
        color_discrete_map=custom_colors
        )

    with open(pr_plot_path, 'wb') as f: 
        pickle.dump(pr_plot_fig, f)

    # prepare residual vs. fitted plot 
    train_results_df = train_df[['in_store_orders']].copy()
    train_results_df['predicted'] = y_train_pred
    train_results_df['resid'] = train_results_df['in_store_orders'] - train_results_df['predicted']

    resid_fig = px.scatter(x=train_results_df['predicted'], y=train_results_df['resid'], width=650)
    resid_fig.add_hline(y=0, line_dash='dash', line_color='red')

    with open(resid_fit_plot_path, 'wb') as f:
        pickle.dump(resid_fig, f)

    # prepare residual distribution plot 
    resid_dist_fig = px.histogram(train_results_df, x='resid', marginal='violin', nbins=35, width=650)

    with open(resid_dist_plot_path, 'wb') as f:
        pickle.dump(resid_dist_fig, f)
    
    print("Successfully generated results for orders prediction!")

if __name__ == "__main__":
    main()