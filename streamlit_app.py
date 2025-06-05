import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(layout="wide")


### Title 

st.title('Litte Pisces sales monitor')


### Side bar elements 
with st.sidebar:

    st.header('Input features')

    temp = st.number_input(
        "What is the forecasted temperature?", value=5
    )

    rain = st.number_input(
        "What is the forecasted rain level?", value=5
    )

    cloud = st.number_input(
        "What is the forecasted cloud coverage level?", value=5
    )

    snow = st.number_input(
        "What is the forecasted snow level?", value=0
    )

    day_of_the_week = st.selectbox(
        "Which day of the week is it?", 
        ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    )

    is_long_weekend = st.selectbox(
         "Is it a long weekend?", 
         (False, True)
    )

    is_HCF = st.selectbox(
         "Is it Hot Chocolate Festival?", 
         (False, True)
    )

    is_holiday = st.selectbox(
        "Is it a Holiday?", 
        (False, True)
    )

    season = st.selectbox(
        "What season is it?", 
        ("Winter", "Spring", "Summer", "Fall")
    )

    has_pop_up = st.selectbox(
    "Will there be a pop up?", 
    (False, True)
    )


### load pickle 
with open("lr_pipe.pickle", 'rb') as f:
        lr_pipe = pickle.load(f)

### making prediction 
data = {
 'hours_opened': 11,
 'avg_temperature': temp,
 'rain': rain,
 'snow': snow,
 'avg_cloud_cover_8': cloud,
 'is_long_weekend': is_long_weekend,
 'is_HCF': is_HCF,
 'has_pop_up': has_pop_up,
 'season': season,
 'day_of_week': day_of_the_week,
 'is_holiday': is_holiday}

input_df = pd.DataFrame(data, index=[0])

input_df

prediction = lr_pipe.predict(input_df)[0]

pred = pd.DataFrame({'predicted sales': prediction}, index=[0])
pred

### Graphs 
total_sales_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/total_sales_df')
combined_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/combined_df', index_col=0, parse_dates=True)
sales_df = combined_df[['total_sales_normalized', 'item_A_sales','item_B_sales', 'item_C_sales']]

### Get last 30 days data 
last_30_df = sales_df.iloc[-30:,:]

last_30_days_sales = px.line(
    last_30_df, 
    title='Daily sales - last 30 days',
    labels={
        'date': 'Date',
        'total_sales_normalized': 'Sales ($)'
    }
)

st.plotly_chart(last_30_days_sales)

#st.line_chart(last_30_df, x='date', y = 'total_sales_normalized')

#st.line_chart(last_30_df, x='date', y = ['item_A_sales', 'item_B_sales', 'item_C_sales'])
