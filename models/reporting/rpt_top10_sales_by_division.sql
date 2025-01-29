{{config(materialized = 'view', schema = 'reporting')}}

select 
c.companyname, c.contactname, c.divisionname, sum(o.linesalesamount) as sales
from
{{ref('fct_orders')}} as o inner join {{ref('dim_customers')}} as c 
on o.customerid = c.customerid 
where c.divisionname = '{{var('v_division', 'Europe')}}'
group by
c.companyname, c.contactname, c.divisionname order by sales desc limit 10