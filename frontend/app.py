import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import show_monthly_analytics

AIP_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["➕ Add/Update", "📊 Analytics by Category", "🗓️ Analytics by Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    show_monthly_analytics()

