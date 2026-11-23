import pandas as pd
from pathlib import Path
from week1_2_cleaning import clean_orders 
from week1_2_cleaning import merge_all

def avg_delv_days_bystate(data,split_column,operation_column,labeled):
	'''calculate average days by states '''

	data=data.copy()
	avg_day_bystate=data.groupby(split_column)[operation_column].mean().reset_index(name=labeled)
	return avg_day_bystate

def filter_table(data,col1,col2):
	'''filter table combining two condition '''

	data=data.copy()
	mask_not_missing=data[col1].notnull()
	mask_delivered=data[col2]=='delivered'
	data=data[(mask_not_missing)&(mask_delivered)]
	return data

def late_delivery(data,col1,col2):
	''' creaete a filter table with relational operation '''

	data=data.copy()
	new_data=data[data[col1]>data[col2]]
	return new_data

if __name__=='__main__':
	# 1 monthly revenue trend(order_purchase_timestamp -- moth,sum payment_value)
	  # load data
	df_orders=clean_orders.load_data(Path('data')/'olist_orders_dataset.csv')
	df_payments=clean_orders.load_data(Path('data')/'olist_order_payments_dataset.csv')

	  # merge(df_payments,df_orders)
	table_payments_orders=merge_all.merge_tables(df_payments,df_orders,'order_id','left','many_to_one')

	  # converting order_purchase_timestamp to datetime 
	table_payments_orders=clean_orders.conv_todatetime(table_payments_orders,'order_purchase_timestamp')
	table_payments_orders['order_purchase_timestamp_month']=table_payments_orders['order_purchase_timestamp'].dt.month_name()
	table_monthly_revenue=merge_all.aggregate_payments(table_payments_orders,'order_purchase_timestamp_month','payment_value','monthly_revenue')
	  # save into CSV
	table_monthly_revenue.to_csv(Path('data')/'monthly_revenue.csv',index=False)

	# 2 top 10 states by total revenue
	'''we merge table_payments_orders with df_customers than we group by column customer_city by total revenue'''
	df_customers=clean_orders.load_data(Path('data')/'olist_customers_dataset.csv')
	table_states=merge_all.merge_tables(table_payments_orders,df_customers,'customer_id','left','many_to_one')

	group_states=merge_all.aggregate_payments(table_states,'customer_state','payment_value','total_revenue')
	top10_state_revenue=group_states.nlargest(10,'total_revenue')
	# save into CSV
	top10_state_revenue.to_csv(Path('data')/'top10_state_revenue.csv',index=False)

	# 3 average delivery days by state
	table_states=clean_orders.add_delv_day(table_states,'order_delivered_customer_date','order_purchase_timestamp','delivery_days')
	  # save it into CSV
	table_states.to_csv(Path('data')/'delivery_days.csv',index=False)

	average_delv_bystate=avg_delv_days_bystate(table_states,'customer_state','delivery_days','average_delivery_daysbystate')
	  # save it into CSV
	average_delv_bystate.to_csv(Path('data')/'average_deivery_days_bystate.csv',index=False)

	# 4 % of orders delivered late
	table_states=clean_orders.conv_todatetime(table_states,'order_estimated_delivery_date')
	delivered_estimated=filter_table(table_states,'order_delivered_customer_date','order_status')
	only_delay=late_delivery(delivered_estimated,'order_delivered_customer_date','order_estimated_delivery_date')
	
	percentage_delay=(len(only_delay)/len(delivered_estimated))
	print(percentage_delay)

	# 5 Payment type distribution
	distribution=table_states.groupby('payment_type').size().reset_index(name='Count').sort_values(by='Count',ascending=False)
	print(distribution)





























