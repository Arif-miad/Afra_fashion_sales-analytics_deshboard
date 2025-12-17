import streamlit as st
import pandas as pd
from PIL import Image

import plotly.express as px

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="AFRA Fashion Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cloth_shop_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------------------------------------------------------
# Banner Image
# ---------------------------------------------------------
banner = Image.open("banner/afra.png")

st.image(
    banner,
    use_container_width=True
)

# ---------------------------------------------------------
# Title Section
# ---------------------------------------------------------
st.title("🧵 AFRA Fashion – Sales Analytics Dashboard")
st.markdown("##### Professional & Interactive Business Intelligence Report")
st.divider()

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("🔎 Filter Options")

# Date Filter
min_date = df["Date"].min()
max_date = df["Date"].max()

start_date = st.sidebar.date_input(
    "📅 Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "📅 End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# City Filter
city = st.sidebar.multiselect(
    "🏙️ Select City",
    options=sorted(df["City"].unique())
)

# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------
filtered_df = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
]

if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
total_sales = filtered_df["Total_Price"].sum()
total_orders = filtered_df["Invoice_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"৳ {total_sales:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📦 Total Quantity", total_quantity)
col4.metric("📊 Avg Order Value", f"৳ {avg_order_value:,.0f}")

st.divider()

# ---------------------------------------------------------
# Charts Section
# ---------------------------------------------------------
st.subheader("📈 Sales Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by City")
    city_sales = (
        filtered_df.groupby("City")["Total_Price"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(city_sales)

with col2:
    st.markdown("### Sales by Item")
    item_sales = (
        filtered_df.groupby("Item")["Total_Price"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(item_sales)

st.divider()

# ---------------------------------------------------------
# Data Table
# ---------------------------------------------------------
st.subheader("📋 Filtered Sales Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    """
    <hr>
    <center>
    © 2024 <b>AFRA Fashion</b> | Built with ❤️ using Streamlit
    </center>
    """,
    unsafe_allow_html=True
)
