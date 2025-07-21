# SweetPulse

## About

**SweetPulse** is a forecasting and analytics tool designed for a Vancouver-based dessert cafe. It provides daily sales and order volume predictions based on weather forecasts in Metro Vancouver, allowing business managers to better plan day-to-day operations. The tool also tracks key business metrics and provides interactive visualizations of sales trends down to the item level, enabling users to identify top-performing products and uncover actionable patterns from sales data.



## Demo



## How to Get Started Locally

If you're interested in running the app locally, follow these high-level steps:

### Option 1: conda virtual environment 

1.  **Clone the repository** to your local machine.

    ``` bash
    git clone git@github.com:awlh18/SweetPulse.git
    ```

2.  **Install dependencies** A environment.yml file has been provided to help you get started. You can install the dependencies by running the following commands from the root directory of this repo:
    ``` bash
    conda env create --file environment.yml
    conda activate sweet_pulse
    ```

3.  **Process data and train forecasting models** Also from the root directory of this repo, run the following commands to process input data and train forecasting models: 

    ``` bash
    make clean
    make all
    ```

4.  **Run the app** Run the dashboard locally by:

    ``` bash
    streamlit run app.py
    ```

5.  **Access the app** You can now run access the app through by:

    ``` bash
    http://localhost:PORT
    ```

6. **Stop the app** To stop the app, press **Ctrl + C** in the terminal. 

### Option 2: Docker container 

1. **Clone the repository** to your local machine.

    ``` bash
    git clone git@github.com:awlh18/SweetPulse.git
    ```
2. Ensure **Docker** is installed and running on your local machine. 

3. **Process data and train forecasting models** From the root directory of this repo, run the following command: 

    ``` bash
    docker-compose up
    ```
4. **Stop the app** To stop the app, press **Ctrl + C** in the terminal, then run:

    ``` bash
    docker-compose down
    ```