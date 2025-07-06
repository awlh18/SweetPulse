import streamlit as st

st.set_page_config(layout="wide")

sales_monitor_page = st.Page("sales_monitor.py", title="Sales monitor", icon=":material/finance_mode:")
diagnostics_page = st.Page("diagnostics.py", title="Model diagnostics", icon=":material/monitor_heart:")

pg = st.navigation({"Page selection":[sales_monitor_page, diagnostics_page]})
pg.run()