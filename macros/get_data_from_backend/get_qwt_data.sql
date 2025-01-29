{% macro get_order_linenos() %}

{% set order_linenos_query %}

select distinct lineno from {{ref('fct_orders')}} order by 1

{% endset %}

{% set results = run_query(order_linenos_query) %}

{% if execute %}

{% set linenos_list = results.columns[0].values() %}

{% else %}

{% set linenos_list = [] %}

{% endif %}

{{ return(linenos_list) }}

{% endmacro %}