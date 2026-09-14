import pandas as pd
from pathlib import Path


# 1-Loading dataset
def load_orders(path):
	'''loading dataset'''
	
	d_f=pd.read_csv(path)
	return d_f 


# 2-parse to datetime	
def conv_todatetime(d_f,col):
	d_f=d_f.copy()

	d_f[col]=pd.to_datetime(d_f[col],errors='coerce')

	return d_f
    


# 3-drop rows fulffil a condition:
# condition: order_dilivered_customer_date "is missing" and order_status "is dilivered" 
def drop_rows(d_f,col1,col2):
	'''drop rows fulfil condition'''
	d_f=d_f.copy()
	mask_miss=d_f[col1].isnull() 
	mask_deli=d_f[col2]=='delivered'
	d_f=d_f.loc[~((mask_miss)&(mask_deli))]
	return d_f
    
 
	
# 4-Create a delivery day columns
def add_delv_day(d_f,delivered,order):
    '''we convert the data column to propre datatype,and we calculate delivery_days'''
    d_f=d_f.copy()
    d_f[delivered]=pd.to_datetime(d_f[delivered],errors='coerce')
    d_f['delivery_days']=(d_f[delivered]-d_f[order]).dt.days
    return d_f


# 5-Remove duplicates on order_id
def rem_dup(d_f,*coll):
	'''removing duplicates from a column'''
	d_f=d_f.copy()
	d_f=d_f.drop_duplicates(subset=coll)
	return d_f

        
if __name__ =='__main__':

	d_f=load_orders(Path('..')/'data'/'olist_orders_dataset.csv')

	d_f=conv_todatetime(d_f,'order_purchase_timestamp')

	d_f=drop_rows(d_f,'order_delivered_customer_date','order_status')

	d_f=add_delv_day(d_f,'order_delivered_customer_date','order_purchase_timestamp')

	d_f=rem_dup(d_f,'order_id')

	d_f.to_csv(Path('..')/'data'/'clean_orders.csv',index=False)

	print(f'saved{len(d_f)}clean orders')

	



'''with open('C:/Users/STS/Documents/ecommerce-project/data/olist_orders_dataset.csv') as f:
    show=f.readline()
print(show)

print('wrong')
print(new_drop['order_id'].duplicated(keep=False).any())

for i in range(3):
    try:
        if i == 3:
            raise ValueError("Oops")
        print("Processing", i)
    finally:
        print("Cleanup for", i)
        # continue here would be invalid

try:
    x = 10   # we use try...finally inside a loop (for or while)
finally:
    (ontinue)

text = "hello"
print(text.split(""))

average = lambda nums: total = sum(nums) / len(nums)
print(average([1, 2, 3]))

'''




