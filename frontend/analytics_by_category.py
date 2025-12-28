import streamlit as st
from datetime import datetime
import requests
import pandas as pd

# FIXED: Typo corrected from AIP_URL to API_URL
API_URL = "https://expense-tracker-api-5p2j.onrender.com"


def analytics_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        # FIXED: Use the correct API_URL variable
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response = response.json()

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]["total"] for category in response],
            "Percentage": [response[category]["percentage"] for category in response]
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        st.header("📊 Expense Breakdown By Categories")

        # FIXED: use_container_width must be True (not 2)
        # Added a check to ensure data exists before plotting to prevent crashes
        if not df_sorted.empty:
            st.bar_chart(data=df_sorted.set_index("Category")["Percentage"], height=500, use_container_width=True)
        else:
            st.warning("No data available for this period.")

        df_sorted["Total"] = df_sorted["Total"].map("\u20B9 {:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}%".format)

        st.table(df_sorted)