
# what the thing(s) that it will let you great in pandas and the best of all(kimi)
import pandas as pd 
from pathlib import Path 
import clean_orders
# loading dataset

# merging five table into one table 

def merge_tables(f_table,s_table,common_column,direction,relationship):
	'''create a merging talbe '''
	master_table=f_table.merge(s_table, on=common_column, how=direction,validate=relationship)
	return master_table

# aggregate payments 'order_id'
def aggregate_payments(data,split_column,operation_column):

	''' we sum payment of each same order_id'''
	data=data.copy()
	aggregate=data.groupby(split_column)[operation_column].sum().reset_index(name='total_payment')
	return aggregate

#handling missing value:fill with 'unknow_category

def fill_missing_product_category(data,col,imputation):
	'''fill missing value in product_category_name with "unknow_category"'''
	data=data.copy()
	data[col]=data[col].fillna(imputation)
	return data

if __name__=='__main__':
	
	df_items=clean_orders.load_orders(Path('..')/'data'/'olist_order_items_dataset.csv')
	df_products=clean_orders.load_orders(Path('..')/'data'/'olist_products_dataset.csv')
	df_payments=clean_orders.load_orders(Path('..')/'data'/'olist_order_payments_dataset.csv')
	df_customers=clean_orders.load_orders(Path('..')/'data'/'olist_customers_dataset.csv')
	df_orders=clean_orders.load_orders(Path('..')/'data'/'olist_orders_dataset.csv')

	master_table=merge_tables(df_orders,df_customers,'customer_id','inner','one_to_one')
	master_table=merge_tables(master_table,df_items,'order_id','right','one_to_many')
	master_table=merge_tables(master_table,df_products,'product_id','left','many_to_one')
	master_table=merge_tables(master_table,df_payments,'order_id','left','many_to_many')

	master_table=clean_orders.rem_dup(master_table,'order_id','order_item_id')


	aggregate=aggregate_payments(master_table,'order_id','payment_value')

	master_table=fill_missing_product_category(master_table,'product_category_name','unknow_category')
	master_table.to_csv(Path('..')/'data'/'master_table.csv',index=False)




