import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

from week1_2_cleaning.clean_orders import load_data ,conv_todatetime
from week1_2_cleaning.merge_all import merge_tables,aggregate_payments
from pathlib import Path

def remove_outdated_rows(data,col,time):
	data=data.copy()
	mask=data[col]>time 
	data=data.loc[~mask]
	return data


if __name__=='__main__':

	## download orders table and convert its columns to propriete datatype and make it clean 

	df_orders=load_data(Path('data')/'clean_orders.csv')
	df_orders.info()

	columns=['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']
	for column in columns:
		df_orders=conv_todatetime(df_orders,column)
	# df_orders.info() delivery_days has only 96476 non-null 

	## download other tables and merge between them 

	# download df_customers
	df_customers=load_data(Path('data')/'olist_customers_dataset.csv')
	df_customers.info()

	# first merge (df_orders and df_customers)
	first_merge=merge_tables(df_orders,df_customers[['customer_id','customer_state']],'customer_id','inner','one_to_one')
	first_merge.info()

	# download df_items
	df_items=load_data(Path('data')/'olist_order_items_dataset.csv')
	df_items.info()
	# converting shipping_limit_date to datetime 
	df_items=conv_todatetime(df_items,'shipping_limit_date')
	df_items.info()
	df_items=remove_outdated_rows(df_items,'shipping_limit_date','2019-01-01 00:00:01')
	df_items.info()
	# remove rows from df_orders that don't match rows in df_items on order_id column
	print(df_orders['order_status'].value_counts())
	# filter rows where order_status equals to canceled ,unavailable or created
	mask_rows=(df_orders['order_status']=='canceled') |(df_orders['order_status']=='unavailable') | (df_orders['order_status']=='created')
	print(mask_rows.sum())
	show_mask=df_orders[['order_id']].loc[mask_rows]
	print(show_mask)
	# Check whether each value in df_orders['order_id'] exists in df_items['order_id']
	checking = show_mask['order_id'].isin(df_items['order_id'])
	# Count matching and non-matching values
	print("Matching:", checking.sum())
	print("Not matching:", (~checking).sum())
	# filtering not mathcing rows from the output of show_mask
	not_matching=show_mask.loc[~checking]
	print(not_matching.index)
	# now droping not matching rows from the df_orders
	df_orders=df_orders.drop(index=not_matching.index)
	df_orders.info()
	# group by order_id in df_items ,the output will merge with first_merge
	df_items=df_items.groupby('order_id').agg(
		
		product_id=('product_id','first'),
		total_price=('price','sum'),
		total_freight=('freight_value','sum')
		).reset_index()
	df_items.info()
	print(type(df_items))
	# second merge (first_merge with df_items)
	second_merge=merge_tables(first_merge,df_items,'order_id','inner','one_to_one')
	second_merge.info()


	# download df_products
	df_products=load_data(Path('data')/'olist_products_dataset.csv')
	df_products.info()
	# third merge (second_merge with df_products)
	third_merge=merge_tables(second_merge,df_products[['product_id','product_category_name']],'product_id','left','many_to_one')
	third_merge.info()
	

	# download df_translation
	df_translation=load_data(Path('data')/'product_category_name_translation.csv')
	df_translation.info()
	# fourth merge (third_merge with df_translation)
	fourth_merge=merge_tables(third_merge,df_translation,'product_category_name','left','many_to_one')
	fourth_merge.info()

	# check from where it comes missing values for the target delivery_days
	# missing values comes from order_status categories except the category delivered 
	mask= (fourth_merge['order_status']=='approved') & (fourth_merge['delivery_days'].isnull())
	show=fourth_merge.loc[mask]
	show.info()
	print(fourth_merge['order_status'].value_counts())

	
	# download df_payments
	df_payments=load_data(Path('data')/'olist_order_payments_dataset.csv')
	df_payments.info()
	# group by order_id and sum payment_value
	df_payments_agg=df_payments.groupby(['order_id'])[['payment_value']].sum().reset_index()
	df_payments_agg.info()
	# final merge (fourth_merge with df_payments_agg)
	final_merge=merge_tables(fourth_merge,df_payments_agg,'order_id','left','one_to_one')
	final_merge.info()
	## we try build our model now

	# remove rows from delivery_days where is null 
	model_data=final_merge.dropna(
		subset=['delivery_days']
		).copy()
	model_data.info()
	# remove rows from payment_value where it is null
	model_data=model_data.dropna(
		subset=['payment_value']
		).copy()
	# Extract the purchase month
	model_data['purchase_month'] = (
		model_data['order_purchase_timestamp'].dt.month
		)
	
	# drop unnecessarily columns
	
	columns_to_drop=[
	'delivery_days',
	'order_delivered_customer_date',
	'order_delivered_carrier_date',
	'order_estimated_delivery_date',
	'order_status',
	'order_purchase_timestamp',
	'order_id',
	'product_category_name',
	'product_id',
	'order_approved_at',
	'customer_id']
	# create X features and y target
	X=model_data.drop(columns=columns_to_drop)
	y=model_data['delivery_days']

	X.info()

	# Split into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=0.2,
		random_state=42
		)
	print(X_test.shape)

	X_test.iloc[[0]].to_csv(
		'week7_8_model/test_order.csv',
		index=False
		)
	'''
	# preprocessing pipeline
	categorical_features =[
	'customer_state',
	'product_category_name_english'
	]

	categorical_transformer = Pipeline(steps=[
		('imputer', SimpleImputer(
			strategy='constant',
			fill_value='Unknown'

		)),
		('onehot', OneHotEncoder(handle_unknown='ignore'))
		])

	preprocessor = ColumnTransformer(
		transformers=[
		('cat', categorical_transformer, categorical_features)
		],
		remainder='passthrough'
		)

	# fitting
	X_train_processed = preprocessor.fit_transform(X_train)
	X_test_processed = preprocessor.transform(X_test)
	print("Training shape:", X_train_processed.shape)
	print("Test shape:", X_test_processed.shape)

	# train the baseline

	baseline = DummyRegressor(strategy='mean')
	baseline.fit(X_train_processed, y_train)

	y_pred_baseline = baseline.predict(X_test_processed)

	mae_baseline = mean_absolute_error(y_test, y_pred_baseline)
	rmse_baseline = np.sqrt(mean_squared_error(y_test, y_pred_baseline))

	print(f"Baseline MAE:  {mae_baseline:.2f} days")
	print(f"Baseline RMSE: {rmse_baseline:.2f} days")

	# Rondom forest
	rf_model = Pipeline(steps=[
		('preprocessor', preprocessor),
		('model', RandomForestRegressor(
			n_estimators=100,
			max_depth=None,
			min_samples_leaf=2,
			random_state=42,
			n_jobs=-1
			))
		])

	rf_model.fit(X_train, y_train)

	# evaluate
	y_pred_rf = rf_model.predict(X_test)

	mae_rf = mean_absolute_error(y_test, y_pred_rf)
	rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

	print(f"Random Forest MAE:  {mae_rf:.2f} days")
	print(f"Random Forest RMSE: {rmse_rf:.2f} days")

	model_path=Path('week7_8_model')/'random_forest_model.joblib'
	joblib.dump(rf_model ,model_path)
	'''








	
    
    
    
    
    
    


	
    

    
    
    

    
    

































