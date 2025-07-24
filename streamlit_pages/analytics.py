import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import datetime



today = datetime.datetime.now()

# title 
st.title('Analytics')

# read in data 
combined_df = pd.read_csv('data/processed/combined.csv', index_col=0, parse_dates=True)
combined_df['sales_per_order'] = combined_df['total_sales_normalized'] / combined_df['in_store_orders'] 
combined_df['month'] = combined_df.index.month_name()
combined_df[combined_df.select_dtypes(include='number').columns] = combined_df[combined_df.select_dtypes(include='number').columns].round(1)

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

with st.sidebar:
    st.markdown('### Select month')


    month_selection = st.selectbox(
        "Select month for analytics",
            ['All', 'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ])

if month_selection == 'All':
    input_df = combined_df 
else:
    input_df = combined_df[combined_df['month'] == month_selection]
         
# sales by day of week 
st.markdown(f'#### Sales Distribution By Day Of Week')

col_1_1, col_1_2 = st.columns(2)

with col_1_1:
    sales_by_day = px.box(input_df, 
                          x='day_of_week', 
                          y='total_sales_normalized', 
                          color='is_holiday', 
                          category_orders={'day_of_week': weekday_order}, 
                          color_discrete_map={False: '#636EFA',  
                                               True: '#EF553B'})

    sales_by_day.update_layout(
    title='Total sales',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Total sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day)

with col_1_2:
    sales_by_day_A = px.box(input_df, 
                            x='day_of_week', 
                            y='item_A_sales', 
                            color='is_holiday', 
                            category_orders={'day_of_week': weekday_order},
                            color_discrete_map={False: '#636EFA',  
                                               True: '#EF553B'})
    sales_by_day_A.update_layout(
    title='Item A sales',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item A sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_A.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_A)

col_2_1, col_2_2 = st.columns(2)

with col_2_1:
   
    sales_by_day_B = px.box(input_df, 
                        x='day_of_week', 
                        y='item_B_sales', 
                        color='is_holiday', 
                        category_orders={'day_of_week': weekday_order},
                        color_discrete_map={False: '#636EFA',  
                                            True: '#EF553B'})
    sales_by_day_B.update_layout(
    title='Item B sales',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item B sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_B.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_B)

with col_2_2:
    sales_by_day_C = px.box(input_df, 
                        x='day_of_week', 
                        y='item_C_sales', 
                        color='is_holiday', 
                        category_orders={'day_of_week': weekday_order},
                        color_discrete_map={False: '#636EFA',  
                                            True: '#EF553B'})
    sales_by_day_C.update_layout(
    title='Item C sales',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Item C sales ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sales_by_day_C.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sales_by_day_C)


st.markdown(f'#### Orders & Sales Per Order By Day Of Week')

col_3_1, col_3_2 = st.columns(2)

with col_3_1:
    order_by_day = px.box(input_df, 
                    x='day_of_week', 
                    y='in_store_orders', 
                    color='is_holiday', 
                    category_orders={'day_of_week': weekday_order},
                    color_discrete_map={False: '#636EFA',  
                                        True: '#EF553B'})
    order_by_day.update_layout(
    title='In store orders',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Number of orders',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    order_by_day.update_yaxes( gridcolor="lightgrey")

    st.plotly_chart(order_by_day)

with col_3_2:
    sop_by_day = px.box(input_df, 
                x='day_of_week', 
                y='sales_per_order', 
                color='is_holiday', 
                category_orders={'day_of_week': weekday_order},
                color_discrete_map={False: '#636EFA',  
                                    True: '#EF553B'})
    sop_by_day.update_layout(
    title='Sales per order',
    xaxis_title='Day of week',
    yaxis=dict(
        title='Sales per order ($)',
        tickformat=','),
    legend_title=dict(text='Holiday'))
    sop_by_day.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(sop_by_day)

st.markdown(f'#### Hot Chocolate Festival Impact On Item Sales (February)')

col_4_1, col_4_2 = st.columns(2)

with col_4_1:
    combined_df_winter = combined_df[combined_df['month'] == 'February']

    A_HCF = px.box(input_df, 
                x='day_of_week', 
                y='item_A_sales', 
                color='is_HCF', 
                category_orders={'day_of_week': weekday_order},
                color_discrete_map={False: '#636EFA',  
                                    True: '#EF553B'})

    A_HCF.update_layout(
        title='HCF on item A sales',
        xaxis_title='Day of week',
        yaxis_title='Item A sales ($)',
        legend_title=dict(text='HCF'))
    A_HCF.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(A_HCF)

with col_4_2:
    combined_df_winter = combined_df[combined_df['month'] == 'February']

    B_HCF = px.box(input_df, 
                x='day_of_week', 
                y='item_B_sales', 
                color='is_HCF', 
                category_orders={'day_of_week': weekday_order},
                color_discrete_map={False: '#636EFA',  
                                    True: '#EF553B'})

    B_HCF.update_layout(
        title='HCF on item B sales',
        xaxis_title='Day of week',
        yaxis_title='Item B sales ($)',
        legend_title=dict(text='HCF'))
    B_HCF.update_yaxes(gridcolor="lightgrey")

    st.plotly_chart(B_HCF)

