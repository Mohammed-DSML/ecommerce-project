import pandas as pd
from pathlib import Path
from week1_2_cleaning import clean_orders 
from week1_2_cleaning import merge_all

def avg_delv_days_bystate(data,split_column,operation_column,labeled):
	'''calculate average days by states 
	-we have two columns one for group similar elements and second for make calculation 
	 - here use mean()
	 -labeled to name our column ,and we use reset_index() to make our output as dataframe'''
	data=data.copy()
	avg_day_bystate=data.groupby(split_column)[operation_column].mean().reset_index(name=labeled)
	return avg_day_bystate

def filter_table(data,col1,col2):
	'''filter table combining two condition  '''
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


''' i got a lot of proplems when i wanted to import modules ,i discoverd to use pyproject.toml and pip install
we create a pyproject.toml file in our root folder (use it when your project has code split across multiple subfolders/packages),
we run this command pip install -e . (editable)flag means any changes
 you make to your python files update instantly without re-installing'''

# 1 monthly revenue trend(order_purchase_timestamp -- moth,sum payment_value)
''' we bring df_orders and df_payments together in one table ,set the key on the columns order_id of df_payments,
we groupe by the column(order_purchase_timestamp) and sum up by the column (payment_value).
i will use the functions that i built and used before in previous module''' 
if __name__=='__main__':
	df_orders=clean_orders.load_data(Path('data')/'olist_orders_dataset.csv')
	df_payments=clean_orders.load_data(Path('data')/'olist_order_payments_dataset.csv')
	table_payments_orders=merge_all.merge_tables(df_payments,df_orders,'order_id','left','many_to_one')
	# converting order_purchase_timestamp to datetime 
	table_payments_orders=clean_orders.conv_todatetime(table_payments_orders,'order_purchase_timestamp')
	table_payments_orders['order_purchase_timestamp_month']=table_payments_orders['order_purchase_timestamp'].dt.month_name()
	#table_payments_orders.info()
	#print(table_payments_orders)
	table_monthly_revenue=merge_all.aggregate_payments(table_payments_orders,'order_purchase_timestamp_month','payment_value','monthly_revenue')
	#table_monthly_revenue.info()
	#print(table_monthly_revenue.sort_values(by='monthly_revenue',ascending=False))
	table_monthly_revenue.to_csv(Path('data')/'monthly_revenue.csv',index=False)

	# 2 top 10 states by total revenue
	'''we merge table_payments_orders with df_customers than we group by column customer_city by total revenue'''
	df_customers=clean_orders.load_data(Path('data')/'olist_customers_dataset.csv')
	table_states=merge_all.merge_tables(table_payments_orders,df_customers,'customer_id','left','many_to_one')
	#table_states.info()
	group_states=merge_all.aggregate_payments(table_states,'customer_state','payment_value','total_revenue')
	top10_state_revenue=group_states.nlargest(10,'total_revenue')
	top10_state_revenue.to_csv(Path('data')/'top10_state_revenue.csv',index=False)
	print(top10_state_revenue)

	# 3 average delivery days by state
	table_states=clean_orders.add_delv_day(table_states,'order_delivered_customer_date','order_purchase_timestamp','delivery_days')
	table_states.to_csv(Path('data')/'delivery_days.csv',index=False)
	# table_states.info()
	
	average_delv_bystate=avg_delv_days_bystate(table_states,'customer_state','delivery_days','average_delivery_daysbystate')
	#print(average_delv_bystate.sort_values(by='average_delivery_daysbystate',ascending=False))

	# 4 % of orders delivered late
	''' first of all we have to determine whick columns we consider in this case ,we have 'order_delivered_customer_date'
	and 'order_estimated_delivery_date' this last we must convert to datetime which let's make comparison
	then we use .loc[] with right condition ,we calculate the sum of all delivered late and devides on total delivered 
	we do all these by using the propriete data in this case is table_states'''
	table_states=clean_orders.conv_todatetime(table_states,'order_estimated_delivery_date')
	#table_states.info()
	delivered_estimated=filter_table(table_states,'order_delivered_customer_date','order_status')
	only_delay=late_delivery(table_states,'order_delivered_customer_date','order_estimated_delivery_date')
	#only_delay.info()
	#delivered_estimated.info()
	percentage_delay=(len(only_delay)/len(delivered_estimated))
	print(percentage_delay)

	# 5 Payment type distribution
	distribution=table_states.groupby('payment_type').size().reset_index(name='Count').sort_values(by='Count',ascending=False)
	print(distribution)





























