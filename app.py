import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import altair as alt

# Page setup
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title(":bulb: Retail Sales Dashboard")

# Loading spinner while fetching data
with st.spinner("Loading data from Snowflake..."):
    # Get the Snowflake session (inside Snowflake-hosted Streamlit)
    session = get_active_session()

    # Load tables into pandas DataFrames
    fact_orders_df = session.table("FACT_ORDERS").to_pandas()
    dim_product_df = session.table("DIM_PRODUCT").to_pandas()
    dim_region_df = session.table("DIM_REGION").to_pandas()

    # Join FACT_ORDERS with DIM_PRODUCT
    merged_df = fact_orders_df.merge(dim_product_df, on="PRODUCT_ID", how="left")

    # Ensure ORDER_DATE is in correct format
    merged_df["ORDER_DATE"] = pd.to_datetime(merged_df["ORDER_DATE"]).dt.date

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Options")

    selected_region = st.multiselect(
        "Select Region",
        options=sorted(dim_region_df["REGION"].unique()),
        default=sorted(dim_region_df["REGION"].unique())
    )

    selected_category = st.multiselect(
        "Select Product Category",
        options=sorted(dim_product_df["CATEGORY"].unique()),
        default=sorted(dim_product_df["CATEGORY"].unique())
    )

    date_range = st.date_input(
        "Select Order Date Range",
        value=(merged_df["ORDER_DATE"].min(), merged_df["ORDER_DATE"].max())
    )

# Apply filters
start_date = pd.Timestamp(date_range[0])
end_date = pd.Timestamp(date_range[1])

filtered_df = merged_df[
    (merged_df["REGION"].isin(selected_region)) &
    (merged_df["CATEGORY"].isin(selected_category)) &
    (pd.to_datetime(merged_df["ORDER_DATE"]) >= start_date) &
    (pd.to_datetime(merged_df["ORDER_DATE"]) <= end_date)
]

# Handle empty result
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- KPIs ---
total_sales = filtered_df["TOTAL_AMOUNT"].sum()
total_orders = filtered_df["ORDER_ID"].nunique()
avg_order_value = filtered_df["TOTAL_AMOUNT"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")




st.subheader("Sales Over Time")
sales_time_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x=alt.X('ORDER_DATE:T', title='Order Date'),
    y=alt.Y('TOTAL_AMOUNT:Q', title='Total Sales'),
    tooltip=['ORDER_DATE', 'TOTAL_AMOUNT']
).interactive().properties(height=350)

st.altair_chart(sales_time_chart, use_container_width=True)

# Sales by Category
st.subheader("Sales by Category")
category_sales = filtered_df.groupby("CATEGORY")["TOTAL_AMOUNT"].sum().reset_index()
category_chart = alt.Chart(category_sales).mark_bar().encode(
    x=alt.X('TOTAL_AMOUNT:Q', title='Total Sales'),
    y=alt.Y('CATEGORY:N', sort='-x'),
    color='CATEGORY:N',
    tooltip=['CATEGORY', 'TOTAL_AMOUNT']
).properties(height=400)

st.altair_chart(category_chart, use_container_width=True)

# Region-wise Sales
st.subheader("Sales by Region")
region_sales = filtered_df.groupby("REGION")["TOTAL_AMOUNT"].sum().reset_index()
region_chart = alt.Chart(region_sales).mark_bar().encode(
    x=alt.X('REGION:N', sort='-y'),
    y=alt.Y('TOTAL_AMOUNT:Q', title='Total Sales'),
    color='REGION:N',
    tooltip=['REGION', 'TOTAL_AMOUNT']
).properties(height=400)

st.altair_chart(region_chart, use_container_width=True)

# --- Raw Data ---
with st.expander("🧾 Show Raw Data"):
    st.dataframe(filtered_df)
