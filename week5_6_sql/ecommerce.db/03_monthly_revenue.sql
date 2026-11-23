# 1- monthly_revenue
-- Question:
-- How much revenue was generated each month?
select month(order_purchase_timestamp) as months,round(sum(payment_value),0) as total
from (
select * 
from olist_order_payments_dataset p 
left join clean_orders o 
    using(order_id)
    ) as joined_data
where order_purchase_timestamp is not null 
group by month(order_purchase_timestamp)
order by months asc;
