import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from week1_2_cleaning import clean_orders

if __name__=='__main__':

    # 1- load data that i need for my charts 
    
    monthly_revenue = clean_orders.load_data(
        Path('data')/ 'monthly_revenue.csv'
        )
    

    top_state=clean_orders.load_data(Path('data')/'top10_state_revenue.csv')
    print(top_state)
    delivery_days=clean_orders.load_data(Path('data')/'delivery_days.csv')

    # 2- 1 Monthly revenue line chart
    # prepare data for visualization 
    months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
    ]
    monthly_revenue['order_purchase_timestamp_month'] = pd.Categorical(
        monthly_revenue['order_purchase_timestamp_month'],
        categories=months,
        ordered=True
        )
    monthly_revenue = monthly_revenue.sort_values(
        'order_purchase_timestamp_month'
        )
    # draw line chart
    fig, ax=plt.subplots(figsize=(12,6))
    ax.plot(monthly_revenue['order_purchase_timestamp_month'],monthly_revenue['monthly_revenue'],'-b')
    ax.set(title='Monthly Revenue',
        xlabel='Month',
        ylabel='Revenue')
    fig.savefig(Path('week3_4_analysis')/'output'/'monthly_revenue.png',dpi=300)
    plt.show()

    # 2- 2 top 10 state bar chart
    # draw bar chart 
    fig, ax= plt.subplots(figsize=(12,6))
    ax.bar(top_state['customer_state'],top_state['total_revenue'])
    ax.set(title='Revenue by top 10 states',
        xlabel='States',
        ylabel='Revenue')
    fig.savefig(Path('week3_4_analysis')/'output'/'top_state.bar.png',dpi=300)
    plt.show()

    # 2- 3 Histogram of delivery days
    # draw histogram chart
    delivery_days.info()
    print(delivery_days['delivery_days'].describe())
    fig, ax=plt.subplots(figsize=(8,4))
    ax.hist(delivery_days['delivery_days'],bins=20,edgecolor='black')
    ax.set(title='Distribution of delivery days',
        xlabel='Days',
        ylabel='Frequencies')
    fig.savefig(Path('week3_4_analysis')/'output'/'delivery_days_histogram.png',dpi=300)
    plt.show()




 









    
    

