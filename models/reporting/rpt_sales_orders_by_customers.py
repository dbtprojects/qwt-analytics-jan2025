import snowflake.snowpark.functions as F
import pandas as pd
import holidays

def is_holiday(date_col):
    french_holidays = holidays.France()
    is_holiday = (date_col in french_holidays)
    return is_holiday

def avg_order_value(sales, orders):

    return sales/orders

def model(dbt, session):
    dbt.config(materialized = 'table', schema = 'reporting', packages = ["holidays"])

    dim_customers_df = dbt.ref('dim_customers')
    fct_orders_df = dbt.ref('fct_orders')

    customers_orders_df = (
    fct_orders_df
    .group_by('customerid')
    .agg(
        F.min(F.col('orderdate')).alias('first_order_date'),
        F.max(F.col('orderdate')).alias('recent_order_date'),
        F.count(F.col('orderid')).alias('total_orders'),
        F.sum(F.col('LineSalesAmount')).alias('total_sales')
        )
    )

    final_df = (
    dim_customers_df.join(customers_orders_df, dim_customers_df.customerid == customers_orders_df.customerid, 'left')
    .select(dim_customers_df.customerid.alias('customerid'),
            dim_customers_df.companyname.alias('companyname'),
            dim_customers_df.contactname.alias('contactname'),
            customers_orders_df.first_order_date.alias('first_order_date'),
            customers_orders_df.recent_order_date.alias('recent_order_date'),
            customers_orders_df.total_orders.alias('total_orders'),
            customers_orders_df.total_sales.alias('total_sales')
        )
    )

    final_df = final_df.withColumn("average_order_value", avg_order_value(final_df["total_sales"], final_df["total_orders"] ))
    
    final_df = final_df.filter(F.col("FIRST_ORDER_DATE").isNotNull())

    final_df = final_df.to_pandas()

    final_df["IS_FIRSTORDERDATE_ON_HOLIDAY"] = final_df["FIRST_ORDER_DATE"].apply(is_holiday)

    return final_df