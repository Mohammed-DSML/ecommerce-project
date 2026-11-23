


from pathlib import Path 
from week1_2_cleaning import clean_orders
# loading dataset

# merging five table into one table 

def merge_tables(f_table,s_table,common_column,direction,relationship):
	'''create a merging talbe '''
	master_table=f_table.merge(s_table, on=common_column, how=direction,validate=relationship)
	return master_table

# aggregate payments 'order_id'
def aggregate_payments(data,split_column,operation_column,labeled):

	''' we sum payment of each same order_id'''
	data=data.copy()
	aggregate=data.groupby(split_column)[operation_column].sum().reset_index(name=labeled)
	return aggregate


#handling missing value:fill with 'unknow_category

def fill_missing_product_category(data,col,imputation):
	'''fill missing value in product_category_name with "unknow_category"'''
	data=data.copy()
	data[col]=data[col].fillna(imputation)
	return data

if __name__=='__main__':

	# 1- load data
	df_items=clean_orders.load_data(Path('data')/'olist_order_items_dataset.csv')
	df_products=clean_orders.load_data(Path('data')/'olist_products_dataset.csv')
	df_payments=clean_orders.load_data(Path('data')/'olist_order_payments_dataset.csv')
	df_customers=clean_orders.load_data(Path('data')/'olist_customers_dataset.csv')
	df_orders=clean_orders.load_data(Path('data')/'olist_orders_dataset.csv')

	# 2- Merge 

	   # merge (df_orders,df_customers)=master_table
	master_table=merge_tables(df_orders,df_customers,'customer_id','left','one_to_one')
	master_table.info()
	original_number=len(df_orders)
	assert len(master_table)==original_number,'the number of rows are wrong'

	  # merge(master_table,aggregate_df_payments(we aggregate df_payments.look below))=master_table
	  # 1-aggregate df_payments:
	aggregate_df_payments=aggregate_payments(df_payments,'order_id','payment_value','total_payment')
	aggregate_df_payments.info()
	assert aggregate_df_payments['order_id'].duplicated().sum()==0 , 'we must have unique value in order_id'
	  
	  # 2- merge
	master_table=merge_tables(master_table,aggregate_df_payments,'order_id','left','one_to_one')
	master_table.info()
	assert len(master_table)==original_number,'number of rows are wrong'

	  # merge(df_items,df_products)=items_products
	items_products=merge_tables(df_items,df_products,'product_id','left','many_to_one')
	items_products.info()
	assert len(items_products)==len(df_items),'number of rows are wrong'
	
	  #Aggregate items to order grain: total price, main category, product count
	  # Fill NaN before grouping
	items_products['product_category_name'] = items_products['product_category_name'].fillna('unknown_category')
	assert items_products['product_category_name'].isnull().sum()==0,"they don't allow for empty values"

	order_items_products=items_products.groupby('order_id',as_index=False).agg({
		'product_category_name':lambda x: x.mode()[0],
		'price':'sum',
		'freight_value':'sum',
		'product_id':'nunique'
		}).rename(columns={
		'product_category_name':'main_product_category_name',
		'price':'total_price',
		'freight_value':'total_freight',
		'product_id':'num_product_id'
		})
	
	
	  # merge (master_table,order_items_products)=master_table

	master_table=merge_tables(master_table,order_items_products,'order_id','left','one_to_one')
	master_table.info()
	assert len(master_table)==original_number,'we must have  same number of rows'

	# 4- handle missing product categories:fill with 'unknown category'

	master_table=fill_missing_product_category(master_table,'main_product_category_name','unknown_category')
	assert master_table['main_product_category_name'].isnull().sum()==0,"they don't allow for empty values"

	# 5- save master_table in csv format
	master_table.to_csv(Path('data')/'master_table.csv',index=False)
	master_table.info()

	




