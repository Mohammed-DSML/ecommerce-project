# week1-2_cleaning/clean_orders.py
import pandas as pd


def clean_orders(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Clean raw orders and compute delivery_days.
    """
    df = pd.read_csv(input_path)
    
    # Parse dates
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    
    # Business rule: delivered orders must have a delivery date
    mask = (
        (df['order_status'] == 'delivered') 
        & (df['order_delivered_customer_date'].isna())
    )
    df = df[~mask].copy()
    
    # Feature engineering
    df['delivery_days'] = (
        df['order_delivered_customer_date'] 
        - df['order_purchase_timestamp']
    ).dt.days
    
    # Save
    df.to_csv(output_path, index=False)
    
    return df


if __name__ == "__main__":
    clean_orders(
        input_path='data/olist_orders_dataset.csv',
        output_path='data/clean_orders.csv'
    )
    print("Done. Cleaned orders saved to data/clean_orders.csv")