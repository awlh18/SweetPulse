# SweetPulse

## About

**SweetPulse** is a forecasting and analytics tool designed for a Vancouver-based dessert cafe. It delivers real-time sales and order volume predictions based on weather forecasts and other operational inputs to inform daily operations planning. SweetPulse also tracks key business metrics and provides various interactive visualizations/graphs at an item level, enabling users to uncover actionable sales patterns.

### Exploratory data analysis 
As part of the project, an exploratory data analysis was conducted to identify key revenue drivers, analyze sales trends, and quantify the impact of weather and business campaigns on sales. A sample report prepared with anonymized data is available [here.](https://awlh18.github.io/SweetPulse/analysis_sample.html)

### Dashboard demo 
![demo](gif/demo.gif)

## Repository structure

The repository is structured as follows: 

- `data/`:
Contains sample raw and processed datasets used for model training and dashboard visualizations, provided for demonstration purposes. 

- `docs/`:
Contains the exploratory data analysis report. 

- `gif/`:
Stores GIF demonstrating dashboard functionality.

- `model/`:
Includes trained forecasting models. 

- `notebooks/`:
Contains Jupyter notebooks used for exploratory data analysis and prototyping/testing forecasting models.

- `results/`:
Holds outputs from scripts, such as model evaluation and validation results.

- `scripts/`:
Contains utility scripts for data processing, feature engineering, model training, prediction, and other automation tasks used throughout the project.

- `src/`:
Contains scripts defining reusable functions for data validation, feature engineering, and other preprocessing tasks used throughout the project.

- `streamlit_pages/`:
Contains scripts that define the pages and layout of the Streamlit dashboard.