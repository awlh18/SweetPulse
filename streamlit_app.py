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

    st.markdown('### Select inputs')

    with st.expander("Forecasting inputs"):

        day = st.date_input(
            "Forecast date",
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

        has_pop_up = st.selectbox(
        "Will there be a pop up?", 
        (False, True)
        )

    with st.expander("Metric inputs"):
         metric_range = st.selectbox(
              "Select day range for KPIs",
              (7, 14, 30)
         )
    
    with st.expander("Graph inputs"):
        graph_range = st.selectbox(
              "Select day range for trend graphs",
              (30, 90, 180)
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
combined_df = pd.read_csv('data/processed/combined_df', index_col=0, parse_dates=True)
sales_df = combined_df[['total_sales_normalized', 'item_A_sales','item_B_sales', 'item_C_sales']]

### define plotting functions 

def make_line_graph(input_df, range, width=400, height=300): 
    graph = px.line(
        input_df.iloc[-range:,:], 
        width=width,   # set width in pixels
        height=height   # set height in pixels
)
    return graph

def make_trend_graph(input_df, range, width=400, height=300): 
    graph = px.line(
        input_df.iloc[-range:].resample("W").mean(),
        width=width,
        height=height
    )
    
    return graph


### average figures 
avg_orders = combined_df['in_store_orders'].iloc[-metric_range:].mean().astype(int)
avg_sales = combined_df['total_sales_normalized'].iloc[-metric_range:].mean().astype(int)
avg_tips = combined_df['tips_normalized'].iloc[-metric_range:].mean().astype(int)

total_sales = combined_df['total_sales_normalized'].iloc[-metric_range:].sum()
total_orders = combined_df['in_store_orders'].iloc[-metric_range:].sum()
avg_sales_per_order = total_sales/total_orders

### deltas compared to previous period 
avg_orders_last_period = combined_df['in_store_orders'].iloc[-metric_range*2:-metric_range].mean().astype(int)
avg_sales_last_period = combined_df['total_sales_normalized'].iloc[-metric_range*2:-metric_range].mean().astype(int)
avg_tips_last_period = combined_df['tips_normalized'].iloc[-metric_range*2:-metric_range].mean().astype(int)

avg_orders_delta = avg_orders - avg_orders_last_period
avg_sales_delta = avg_sales - avg_sales_last_period
avg_tips_delta = avg_tips - avg_tips_last_period

total_sales_last_period = combined_df['total_sales_normalized'].iloc[-metric_range*2:-metric_range].sum()
total_orders_last_period = combined_df['in_store_orders'].iloc[-metric_range*2:-metric_range].sum()
avg_sales_per_order_last_period = total_sales_last_period / total_orders_last_period
avg_sales_per_order_delta = avg_sales_per_order - avg_sales_per_order_last_period

### prediction 
st.markdown('### Sales forecast')
st.metric(label= "Forecasted sales based on inputs", value=f"${prediction:,}")


### metric boxes 
st.markdown('### KPIs')

col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)

with col_1_1:
      st.metric(label= f"Average daily sales - last {metric_range} days", value=f"${avg_sales:,}", delta=int(avg_sales_delta), border=True)

with col_1_2: 
     st.metric(label= f"Average daily tips - last {metric_range} days", value=f"${avg_tips:,}", delta=int(avg_tips_delta), border=True)

with col_1_3:
     st.metric(label= f"Average daily orders - last {metric_range} days", value=f"{avg_orders:,}", delta=int(avg_orders_delta), border=True)

with col_1_4: 
     st.metric(label= f"Sales per order - last {metric_range} days", value=f"${avg_sales_per_order.round(2):,}", delta=round(avg_sales_per_order_delta, 1), border=True)


### line graphs - sales and orders 

# sales_graph = make_line_graph(sales_df, graph_range)
# sales_graph.update_layout(
#     title = f'Sales - Last {graph_range} days',
#     xaxis_title='Date',
#     yaxis_title='Sales ($)',
#     legend=dict(
#     orientation='h',         # horizontal
#     yanchor='top',
#     y=-0.5,                  # adjust vertical position
#     xanchor='center',
#     x=0.5                    # center the legend
#     )
# )

# orders_graph = make_line_graph(combined_df[['in_store_orders']], graph_range)
# orders_graph.update_layout(
#     title = f'Orders - Last {graph_range} days',
#     xaxis_title='Date',
#     yaxis_title='Number of orders',
#     showlegend=False
# )
# col_2_1, col_2_2 = st.columns(2)

# with col_2_1:   
#     st.plotly_chart(sales_graph)
# with col_2_2:
#     st.plotly_chart(orders_graph)

### line graphs - trends 

sales_trend_graph = make_trend_graph(sales_df, graph_range, height=320)
sales_trend_graph.update_layout(
    title = f'Weekly sales trend - last {graph_range} days',
    xaxis_title='Date',
    yaxis_title='Sales ($)',
    legend=dict(
    orientation='h',         # horizontal
    yanchor='top',
    y=-0.5,                  # adjust vertical position
    xanchor='center',
    x=0.5                    # center the legend
    )
)

orders_trend_graph = make_trend_graph(combined_df[['in_store_orders']], graph_range, height=270)
orders_trend_graph.update_layout(
    title = f'Weekly orders trend - last {graph_range} days',
    xaxis_title='Date',
    yaxis_title='Orders',
    showlegend=False
)

col_3_1, col_3_2 = st.columns(2)

with col_3_1:
    st.plotly_chart(sales_trend_graph)

with col_3_2:
    st.plotly_chart(orders_trend_graph)


