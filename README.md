# SweetPulse

## About

**SweetPulse** is a forecasting and analytics tool designed for a Vancouver-based dessert cafe. It delivers real-time sales and order volume predictions based on weather forecasts and other operational inputs to inform daily operations planning. SweetPulse also tracks key business metrics and provides various interactive visualizations/graphs at an item level, enabling users to uncover actionable sales patterns.

Additionally, the model diagnostic pages help users monitor the performance and validity of each forecasting model, supporting future retraining and model selection.

### Demo
![demo](gif/demo.gif)


## How to Get Started Locally

If you're interested in running the app locally, follow these high-level steps:

### Option 1: conda virtual environment 

1.  **Clone the repository** to your local machine.

    ``` bash
    git clone git@github.com:awlh18/SweetPulse.git
    ```

2.  **Install dependencies:** A environment.yml file has been provided to help you get started. You can install the dependencies by running the following commands from the root directory of this repo:
    ``` bash
    conda env create --file environment.yml
    conda activate sweet_pulse
    ```

3.  **Process data and train forecasting models:** Also from the root directory of this repo, run the following commands to process input data and train the forecasting models: 

    ``` bash
    make clean
    make all
    ```

4.  **Run the dashboard locally** by running the following command from the root directory:

    ``` bash
    streamlit run app.py
    ```

5.  **Access the app:** You can now run access the app through:

    ``` bash
    http://localhost:8501
    ```

6. **Stop the app** To stop the app, press **Ctrl + C** in the terminal. 

### Option 2: Docker container 

1. **Clone the repository** to your local machine.

    ``` bash
    git clone git@github.com:awlh18/SweetPulse.git
    ```
2. Ensure **Docker** is installed and running on your local machine. 

3. **Process data and train forecasting models:** From the root directory of this repo, run the following command: 

    ``` bash
    docker-compose up
    ```
4. To **stop the app**, press **Ctrl + C** in the terminal, then run:

    ``` bash
    docker-compose down
    ```