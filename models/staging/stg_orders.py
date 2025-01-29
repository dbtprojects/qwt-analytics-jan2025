import snowflake.snowpark.functions as F

def model(dbt, session):

    dbt.config(materialized = 'incremental', unique_key = 'orderid')
    df_orders = dbt.source("qwt_raw", "raw_orders")

    if dbt.is_incremental:

        max_order_date = f"select max(orderdate) from {dbt.this}"

        df_orders = df_orders.filter(df_orders.orderdate > session.sql(max_order_date).collect()[0][0])

    return df_orders
