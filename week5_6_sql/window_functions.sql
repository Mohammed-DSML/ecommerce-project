


 -- WINDOW FUNCTIONs
 ----
 # 1- running total revenue by month for each year
 

select * ,
round(sum(payment_value) over(partition by month(order_purchase_timestamp),year(order_purchase_timestamp)),0) as total_revenue 
from olist_order_payments_dataset p 
left join  orders o
using(order_id)
where order_purchase_timestamp is not null ;

--
# 2- Rank customers by lifetime spend per state 

select customer_id,customer_state,total,
Rank() Over(
partition by customer_state 
order by total DESC) as customer_rank
from(
select  customer_id,customer_state, round(sum(payment_value),0) as total
from (
select customer_id,customer_state,payment_value
from clean_orders c 
right join olist_order_payments_dataset p
using(order_id) 
left join customers s 
using(customer_id)
where customer_state is not null) as dd
group by customer_id,customer_state) as jj;
-- 
# 3- 3-month rolling average 

select months,years,total ,round(avg(total) over(partition by years
order by months
rows between 2 preceding and current row),0) as rolling_aberage_3month 
from(
select month(order_purchase_timestamp) as months,year(order_purchase_timestamp) as years,round(sum(payment_value),0) as total
from (
select * 
from olist_order_payments_dataset p 
left join clean_orders o 
    using(order_id)
    ) as joined_data
where order_purchase_timestamp is not null 
group by months,years
order by years ,months asc) as dd ;















