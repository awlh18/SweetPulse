import streamlit as st

st.set_page_config(layout="wide")

sales_monitor_page = st.Page("streamlit_pages/sales_monitor.py", title="Sales monitor", icon=":material/finance_mode:")
diagnostics_total_page = st.Page("streamlit_pages/diagnostics_total_sales.py", title="Model diagnostics - Total Sales", icon=":material/monitor_heart:")
diagnostics_item_A_page = st.Page("streamlit_pages/diagnostics_item_A.py", title="Model diagnostics - Item A Sales", icon=":material/monitor_heart:")
diagnostics_item_B_page = st.Page("streamlit_pages/diagnostics_item_B.py", title="Model diagnostics - Item B Sales", icon=":material/monitor_heart:")
diagnostics_orders_page = st.Page("streamlit_pages/diagnostics_orders.py", title="Model diagnostics - In Store Orders", icon=":material/monitor_heart:")

pg = st.navigation({"Page selection":[sales_monitor_page, diagnostics_total_page, diagnostics_item_A_page, diagnostics_item_B_page,
                                      diagnostics_orders_page]})
pg.run()