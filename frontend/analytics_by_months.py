import streamlit as st
import requests
import pandas as pd

API_URL = "https://expense-tracker-api-5p2j.onrender.com"


def show_monthly_analytics():
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)
    df_sorted = df.sort_values(by="Month Number", ascending=True)
    df_sorted.set_index("Month Number", inplace=True)

    st.header("🗓️ Expense Breakdown By Months")

st.bar_chart(data=df_sorted.set_index("Month Name")['Total'], use_container_width=True)

    df_sorted["Total"] = df_sorted["Total"].map("\u20B9 {:.2f}".format)

    st.table(df_sorted.sort_index())
