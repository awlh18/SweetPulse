# SweetPulse

Welcome to **SweetPulse**! 

**SweetPulse** is a forecasting and analytics tool designed to help Vancouver-based restaurants and cafés make data-informed business decisions. It provides daily sales and order volume predictions based on weather forecasts in Metro Vancouver, allowing owners to better plan day-to-day operations.

SweetPulse also tracks key business metrics and provides interactive visualizations of sales trends down to the item level, enabling users to identify top-performing products and uncover actionable patterns in their sales data.


### How to Get Started Locally

If you're interested in running the app locally or contributing to its development, follow these high-level steps:

1.  **Clone the repository** to your local machine.

    ``` bash
    git clone git@github.com:UBC-MDS/DSCI-532_2025_13_Maple-Eagle-Trade-Tracker.git
    ```

2.  **Install dependencies** We have provided a environment.yaml file to help you get started. You can install the dependencies by running:

    ``` bash
    conda env create --file environment.yml
    conda activate sweet_pulse
    ```

3.  **Process data and train forecasting models** Load the latest sales data and weather in the xxx directory and run the following: 

    ``` bash
    make clean
    make all
    ```

4.  **Run the app** Once the dependencies are installed, you can run the dashboard locally with **the root of this repo** set as the current directory:

    ``` bash
    streamlit run app.py
    ```