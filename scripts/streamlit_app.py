import streamlit as st
import pandas as pd
import plotly.express as px

### Title 
st.title('Litte Pisces sales monitor')

### Side bar elements 
with st.sidebar:

    st.header('Input features')

    temp = st.number_input(
        "What is the forecasted temperature?", value=None
    )

    rain_slider = st.slider(
        'What is the forecasted rain level?',
        0.0, 100.0, (25.0, 75.0)
    )

    cloud_slider = st.slider(
        'What is the forecasted cloud coverage?',
        0.0, 100.0, (25.0, 75.0)
    )

### Graphs 
total_sales_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/total_sales_df')
combined_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/combined_df')

last_30_df = combined_df.iloc[-30:,:]

row1_1, row1_2 = st.columns((1,1))

with row1_1:
    st.line_chart(last_30_df, x='date', y = 'total_sales_normalized')

with row1_2:
    st.line_chart(last_30_df, x='date', y = ['item_A_sales', 'item_B_sales', 'item_C_sales'])
