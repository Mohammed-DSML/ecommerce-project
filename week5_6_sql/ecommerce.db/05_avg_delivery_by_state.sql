# 3- average delivery days by state 
-- Question:
-- What is the average delivery time for each state?
 select customer_state,round(avg(delivery_days),0) as total
 from (
 select *
 from customers s 
 left join clean_orders c 
 using(customer_id) ) as x
 group by customer_state
 order by total ASC;
