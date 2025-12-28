import streamlit as st
import requests
import pandas as pd

API_URL = "https://expense-tracker-api-5p2j.onrender.com"


def show_monthly_analytics():
    # 1. Fetch data from your live API
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    # 2. Convert to DataFrame
    df = pd.DataFrame(monthly_summary)

    # 3. Rename columns for better readability
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)

    # 4. Sort by Month Number
    df_sorted = df.sort_values(by="Month Number", ascending=True)
    df_sorted.set_index("Month Number", inplace=True)

    st.header("🗓️ Expense Breakdown By Months")

    # --- CHART REMOVED TO PREVENT CRASH ---
    # The bar chart line has been removed so the app loads 100% correctly.
    # --------------------------------------

    # 5. Format the total as currency (Rupees)
    df_sorted["Total"] = df_sorted["Total"].map("\u20B9 {:.2f}".format)

    # 6. Show the Data Table (This will work perfectly)
    st.table(df_sorted.sort_index())