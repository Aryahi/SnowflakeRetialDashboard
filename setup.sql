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

COPY INTO retail_sales_data
FROM RETAIL_ANALYTICS_DB.PUBLIC@my_internal_stage/retail_sales_data.csv
FILE_FORMAT = (FORMAT_NAME = CSV_COMMA_ONEHEADROW);

create database util_db;

USE DATABASE RETAIL_ANALYTICS_db;
USE SCHEMA PUBLIC;

COPY INTO retail_analytics_db.sales_data.retail_sales_data
FROM @util_db.public.my_internal_stage/retail_sales_data.csv
FILE_FORMAT = util_db.public.CSV_COMMA_ONEHEADROW;

select * from retail_analytics_db.sales_data.retail_sales_data;

USE DATABASE RETAIL_ANALYTICS_DB;
USE SCHEMA SALES_DATA;

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
SELECT DISTINCT
    REGION
FROM RETAIL_SALES_DATA;



