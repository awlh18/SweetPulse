import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import datetime
from sklearn.metrics import mean_absolute_error
from src.feature_functions import *


today = datetime.datetime.now()

# title 
st.title('Sales Monitor')

# side bar elements 
with st.sidebar:
    st.markdown('### Select inputs')

    with st.expander("Forecasting inputs"):

        day = st.date_input(
            "Forecast date",
            format='DD.MM.YYYY'
        )

        hours = st.number_input(
            "Store opening hours", value=11, min_value=0, max_value=24
        )

        temp = st.number_input(
            "What is the forecasted temperature?", value=5, min_value=-50, max_value=50
        )

        rain = st.number_input(
            "What is the forecasted rain level?", value=5, min_value=0, max_value=100
        )

        snow = st.number_input(
            "What is the forecasted snow level?", value=0, min_value=0, max_value=100
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

    with st.expander("KPI inputs"):
         metric_range = st.selectbox(
              "Select day range for KPIs",
              (7, 14, 30, 90, 180),
              index=2
         )
    
    with st.expander("Graph inputs"):
        aggregation_level = st.selectbox(
              "Select aggregation level for trend graphs",
              ('Weekly', 'Monthly')
         )
         
# Making prediction 
day_of_the_week = day.strftime('%A')
season = get_season(day)

data = {
 'hours_opened': hours,
 'avg_temperature': temp,
 'rain': rain,
 'snow': snow,
 'is_long_weekend': is_long_weekend,
 'is_HCF': is_HCF,
 'season': season,
 'day_of_week': day_of_the_week,
 'is_holiday': is_holiday}

input_df = pd.DataFrame(data, index=[0])

# loading in sales data for plots
sales_df = pd.read_csv('data/processed/sales.csv', index_col=0, parse_dates=True)

# define plotting functions 
def make_line_graph(input_df, range, width=400, height=300): 
    graph = px.line(
        input_df.iloc[-range:,:], 
        width=width,   # set width in pixels
        height=height   # set height in pixels
)
    return graph

def make_trend_graph(input_df, agg, width=400, height=300): 
    graph = px.line(
        input_df.resample(agg).mean(),
        width=width,
        height=height
    )
    
    return graph

# show predictions

# load pickles 
with open("model/lr_pipe_total_sales.pkl", 'rb') as f:
        lr_pipe_total = pickle.load(f)

with open("model/lr_pipe_item_A_sales.pkl", 'rb') as f:
        lr_pipe_A = pickle.load(f)

with open("model/lr_pipe_item_B_sales.pkl", 'rb') as f:
        lr_pipe_B = pickle.load(f)

with open("model/pr_pipe_orders.pkl", 'rb') as f:
        pr_pipe = pickle.load(f)

prediction_total = lr_pipe_total.predict(input_df)[0].astype(int)
prediction_A = lr_pipe_A.predict(input_df)[0].astype(int)
prediction_B = lr_pipe_B.predict(input_df)[0].astype(int)
prediction_order = pr_pipe.predict(input_df)[0].astype(int)

st.markdown('### Forecasts')
st.markdown('Based on forecasting input selected')

col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)

with col_1_1:
    st.metric(label= "Total sales", value=f"${prediction_total:,}", border=True)

with col_1_2:
    st.metric(label= "Item A sales", value=f"${prediction_A:,}", border=True)

with col_1_3:
    st.metric(label= "Item B sales", value=f"${prediction_B:,}", border=True)

with col_1_4:
    st.metric(label= "Total orders", value=f"{prediction_order}", border=True)

# metric boxes 

# calculate average figures 
avg_orders = sales_df['in_store_orders'].iloc[-metric_range:].mean().astype(int)
avg_sales = sales_df['total_sales_normalized'].iloc[-metric_range:].mean().astype(int)
avg_tips = sales_df['tips_normalized'].iloc[-metric_range:].mean().astype(int)

total_sales = sales_df['total_sales_normalized'].iloc[-metric_range:].sum()
total_orders = sales_df['in_store_orders'].iloc[-metric_range:].sum()
avg_sales_per_order = total_sales/total_orders

# calculate deltas compared to previous period 
avg_orders_last_period = sales_df['in_store_orders'].iloc[-metric_range*2:-metric_range].mean().astype(int)
avg_sales_last_period = sales_df['total_sales_normalized'].iloc[-metric_range*2:-metric_range].mean().astype(int)
avg_tips_last_period = sales_df['tips_normalized'].iloc[-metric_range*2:-metric_range].mean().astype(int)

avg_orders_delta = avg_orders - avg_orders_last_period
avg_sales_delta = avg_sales - avg_sales_last_period
avg_tips_delta = avg_tips - avg_tips_last_period

total_sales_last_period = sales_df['total_sales_normalized'].iloc[-metric_range*2:-metric_range].sum()
total_orders_last_period = sales_df['in_store_orders'].iloc[-metric_range*2:-metric_range].sum()
avg_sales_per_order_last_period = total_sales_last_period / total_orders_last_period
avg_sales_per_order_delta = avg_sales_per_order - avg_sales_per_order_last_period

st.markdown(f'#### Key Performance Metrics')
st.markdown(f'###### Last {metric_range} days')
st.markdown('(Delta vs. preceding period)')

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)

with col_2_1:
      st.metric(label= f"Average daily sales", value=f"${avg_sales:,}", delta=int(avg_sales_delta), border=True)

with col_2_2: 
     st.metric(label= f"Average daily tips", value=f"${avg_tips:,}", delta=int(avg_tips_delta), border=True)

with col_2_3:
     st.metric(label= f"Average daily orders", value=f"{avg_orders:,}", delta=int(avg_orders_delta), border=True)

with col_2_4: 
     st.metric(label= f"Sales per order", value=f"${avg_sales_per_order.round(2):,}", delta=round(avg_sales_per_order_delta, 1), border=True)

# line graph - weekly sales trends 

if aggregation_level == 'Weekly':
    agg='W'
else:
    agg='M'

core_product_sales = sales_df[['total_sales_normalized', 'item_A_sales', 'item_B_sales', 'item_C_sales']]

sales_trend_graph = make_trend_graph(core_product_sales, agg, height=320)
sales_trend_graph.update_layout(
    title=f'{aggregation_level} sales trend',
    xaxis_title='Date',
    yaxis_title='Total sales ($)',
    width=1230,
    height=500,
    legend=dict(
    orientation='h',         # horizontal
    yanchor='top',
    y=-0.5,                  # adjust vertical position
    xanchor='center',
    x=0.5                    # center the legend
    )
)
sales_trend_graph.update_yaxes( gridcolor="lightgrey")


#  line graph - number of orders vs sales per order trend 

sales_df['sales_per_order'] = sales_df['total_sales_normalized'] / sales_df['in_store_orders']
grouped_df = sales_df.resample(agg).mean(numeric_only=True)
sales_sop = make_subplots(specs=[[{"secondary_y": True}]])
sales_sop.add_trace(go.Line(x=grouped_df.index, y=grouped_df['in_store_orders'], name='number of orders', mode='lines'))
sales_sop.add_trace(go.Line(x=grouped_df.index, y=grouped_df['sales_per_order'], name='sales per order', mode='lines', line=dict(color='red')), 
                    secondary_y=True)


sales_sop.update_layout(
    title=f'{aggregation_level} orders vs. sales per order',
    yaxis=dict(
        title='Orders'
    ),
    yaxis2=dict(
        title='Sales per order'
    ),
    width=1230,
    height=500,
    legend=dict(
        orientation='h',         # horizontal
        yanchor='top',
        y=-0.5,                  # adjust vertical position
        xanchor='center',
        x=0.5                    # center the legend
    )
)

sales_sop.update_yaxes( gridcolor="lightgrey")

col_3_1, col_3_2 = st.columns(2)

with col_3_1:
    st.plotly_chart(sales_trend_graph)

with col_3_2:
    st.plotly_chart(sales_sop)

