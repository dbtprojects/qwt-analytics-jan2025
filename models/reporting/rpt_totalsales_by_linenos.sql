{{config(materialized = 'view', schema = 'reporting')}}

{% set linenumbers = get_order_linenos() %}

select orderid,

{% for linenumber in linenumbers %}

sum(case when lineno = {{linenumber}} then linesalesamount end) as lineno{{linenumber}}_amount,

{% endfor %}

sum(linesalesamount) as total_amount

from {{ref('fct_orders')}}

group by 1