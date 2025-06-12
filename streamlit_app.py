import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import datetime

st.set_page_config(layout="wide")

today = datetime.datetime.now()
### functions 

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

### Title 

st.title('Litte Pisces sales monitor')

### Side bar elements 
with st.sidebar:

    with st.expander("Forecast Inputs"):

        day = st.date_input(
            "Which day would you like to forecast?",
            format='DD.MM.YYYY'
        )

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

        # day_of_the_week = st.selectbox(
        #     "Which day of the week is it?", 
        #     ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        # )

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

        # season = st.selectbox(
        #     "What season is it?", 
        #     ("Winter", "Spring", "Summer", "Fall")
        # )

        has_pop_up = st.selectbox(
        "Will there be a pop up?", 
        (False, True)
        )

    with st.expander("Dashboard Inputs"):
         dashboard_range = st.selectbox(
              "Select day range for dashboard",
              (7, 14, 30)
         )

### load pickle 
with open("lr_pipe.pickle", 'rb') as f:
        lr_pipe = pickle.load(f)

### making prediction 

day_of_the_week = day.strftime('%A')
season = get_season(day)

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

prediction = lr_pipe.predict(input_df)[0].astype(int)

### loading in data
total_sales_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/total_sales_df')
combined_df = pd.read_csv('/Users/alexwong/Desktop/little_picses/restaurant_sales_forecast/data/processed/combined_df', index_col=0, parse_dates=True)
sales_df = combined_df[['total_sales_normalized', 'item_A_sales','item_B_sales', 'item_C_sales']]

### get sales data

sales_graph = px.line(
    sales_df.iloc[-dashboard_range:,:], 
    title=f'Daily sales - last {dashboard_range} days',
    labels={
        'date': 'Date',
        'total_sales_normalized': 'Sales ($)'
    }
)

orders_graph = px.line(
    combined_df[['in_store_orders']].iloc[-dashboard_range:,:], 
    title=f'Daily orders - last {dashboard_range} days',
    labels={
        'date': 'Date',
        'total_sales_normalized': 'Orders'
    }
)

avg_orders = combined_df['in_store_orders'].iloc[-dashboard_range:].mean().astype(int)
avg_sales = combined_df['total_sales_normalized'].iloc[-dashboard_range:].mean().astype(int)
avg_tips = combined_df['tips_normalized'].iloc[-dashboard_range:].mean().astype(int)

total_sales = combined_df['total_sales_normalized'].iloc[-dashboard_range:].sum()
total_orders = combined_df['in_store_orders'].iloc[-dashboard_range:].sum()

avg_sales_per_order = total_sales/total_orders

### metric boxes 
col1, col2, col3, col4 = st.columns(4)

with col1:
      st.metric(label= f"Average daily sales - last {dashboard_range} days", value=f"${avg_sales:,}")

with col2: 
     st.metric(label= f"Average daily tips - last {dashboard_range} days", value=f"${avg_tips:,}")

with col3:
     st.metric(label= f"Average daily orders - last {dashboard_range} days", value=f"{avg_orders:,}")

with col4: 
     st.metric(label= f"Sales per order - last {dashboard_range} days", value=f"${avg_sales_per_order.round(2):,}")

st.plotly_chart(sales_graph)
st.plotly_chart(orders_graph)

#st.line_chart(last_30_df, x='date', y = 'total_sales_normalized')

#st.line_chart(last_30_df, x='date', y = ['item_A_sales', 'item_B_sales', 'item_C_sales'])
