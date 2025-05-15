# 📊 Retail Sales Dashboard

A fully interactive sales analytics dashboard built using **Streamlit**, **Snowflake Snowpark**, **Pandas**, and **Altair**. This dashboard allows users to explore and visualize retail sales data with dynamic filters and KPIs, all hosted directly inside Snowflake (no external server needed).

---

## 🚀 Features

- 📆 **Date Range Filtering** – Explore data across custom time ranges.
- 🌍 **Region Filter** – View sales performance across different regions.
- 🏷 **Category Filter** – Analyze category-wise product performance.
- 💰 **Dynamic KPIs** – See real-time totals for:
  - Total Sales
  - Total Orders
  - Average Order Value
- 📈 **Sales Over Time** – Interactive time-series chart.
- 📦 **Category-Wise Sales** – Bar chart for product categories.
- 🌐 **Region-Wise Sales** – Regional performance comparison.
- 🧾 **Raw Data Viewer** – Toggle to inspect underlying data.

---

## 🧱 Tech Stack

| Tool           | Purpose                                |
|----------------|----------------------------------------|
| **Streamlit**  | Interactive frontend UI and app logic  |
| **Snowflake**  | Cloud data warehouse and compute       |
| **Snowpark**   | Python API for querying Snowflake       |
| **Pandas**     | Data manipulation                      |
| **Altair**     | Declarative data visualization         |

---

## 📂 Project Structure
📁 retail-sales-dashboard/
│
├── 📄 streamlit_app.py # Main Streamlit app script
├── 📄 README.md # Project overview (this file)
├── 📄 requirements.txt # Python dependencies (optional)
└── 📊 Snowflake objects:
├── DATABASE: retail_analytics_db
├── SCHEMA: sales_data
├── TABLES:
│ ├── FACT_ORDERS
│ ├── DIM_PRODUCT
│ └── DIM_REGION


---

## 🛠 Setup Instructions

### 🧭 Snowflake Setup

1. **Create Database & Tables**:

```sql
CREATE DATABASE retail_analytics_db;
CREATE SCHEMA sales_data;

CREATE OR REPLACE TABLE retail_sales_data (
  order_id STRING,
  product_id STRING,
  product_name STRING,
  category STRING,
  region STRING,
  quantity INTEGER,
  price FLOAT,
  order_date DATE
);
Load CSV data into retail_sales_data using Snowflake's COPY INTO.

Create Dimension and Fact Tables:
USE DATABASE retail_analytics_db;
USE SCHEMA sales_data;

CREATE OR REPLACE TABLE FACT_ORDERS AS
SELECT
    ORDER_ID,
    PRODUCT_ID,
    REGION,
    QUANTITY,
    PRICE,
    QUANTITY * PRICE AS TOTAL_AMOUNT,
    ORDER_DATE
FROM RETAIL_SALES_DATA;

CREATE OR REPLACE TABLE DIM_PRODUCT AS
SELECT DISTINCT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY
FROM RETAIL_SALES_DATA;

CREATE OR REPLACE TABLE DIM_REGION AS
SELECT DISTINCT REGION FROM RETAIL_SALES_DATA;

▶️ Running the App
If running inside Snowflake Native App (hosted Streamlit):

No setup needed — simply open the Streamlit app in your Snowflake worksheet.

If running locally (optional):

bash
Copy
Edit
pip install -r requirements.txt
streamlit run streamlit_app.py
You'll need a valid Snowflake connection locally, which is not required inside Snowflake Native Streamlit.

![image](https://github.com/user-attachments/assets/07b2f0f2-79b0-4916-a664-ce96fa9d090a)

