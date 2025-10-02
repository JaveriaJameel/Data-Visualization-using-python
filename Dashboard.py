# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
# Load dataset (replace with your Superstore file path)
df = pd.read_csv("./Sample - Superstore.csv", encoding="ISO-8859-1")


# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
# Title and layout
st.set_page_config(page_title="📊 Superstore Dashboard", layout="wide")
st.title("📊 Superstore Sales Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filters")
region = st.sidebar.multiselect("Select Region:", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", options=df["Category"].unique(), default=df["Category"].unique())

# Apply filters
df_filtered = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]
# KPIs
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
total_orders = df_filtered["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)
# scales by regions
sales_region = df_filtered.groupby("Region")["Sales"].sum().reset_index()
fig_region = px.bar(sales_region, x="Region", y="Sales", color="Region", title="Sales by Region")
st.plotly_chart(fig_region, use_container_width=True)
#monthly sales trend
df_filtered["YearMonth"] = df_filtered["Order Date"].dt.to_period("M").astype(str)
sales_trend = df_filtered.groupby("YearMonth")["Sales"].sum().reset_index()

fig_trend = px.line(sales_trend, x="YearMonth", y="Sales", title="Monthly Sales Trend", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)
#Profit vs Discount Scatter Plo
fig_scatter = px.scatter(df_filtered, x="Discount", y="Profit", size="Sales",
                         color="Category", hover_data=["Sub-Category"],
                         title="Profit vs Discount")
st.plotly_chart(fig_scatter, use_container_width=True)
#Category-wise Sales
sales_category = df_filtered.groupby("Category")["Sales"].sum().reset_index()
fig_category = px.pie(sales_category, names="Category", values="Sales", title="Sales Share by Category")
st.plotly_chart(fig_category, use_container_width=True)



