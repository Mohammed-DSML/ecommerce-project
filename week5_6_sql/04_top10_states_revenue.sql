# 2- top 10 states by total revenue
-- Question:
-- Which 10 states generate the most revenue?

select customer_state ,round(sum(payment_value),0) as revenue
from(
select *
from clean_orders c 
right join olist_order_payments_dataset p
using(order_id) 
left join customers s 
using(customer_id)
where customer_state is not null) as b
group by customer_state
order by revenue DESC
limit 10;