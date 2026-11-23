
import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd

# function query

def run_query(cursor,query):
    '''exectue the query,bring the output to python ,display in tabular form dataframe'''
    cursor.execute(query)
    columns=[column[0] for column in cursor.description]
    results=cursor.fetchall()
    df=pd.DataFrame(results,columns=columns)
    return df

if __name__=='__main__':
    connection = None
    cursor = None
    try:
        load_dotenv()
        
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
            )

        cursor = connection.cursor()
        
        monthly_revenue ="""
        WITH monthly_summary AS (
            SELECT
            YEAR(order_purchase_timestamp) AS yr,
            MONTH(order_purchase_timestamp) AS mn,
            ROUND(SUM(payment_value), 0) AS monthly_revenue
            FROM olist_order_payments_dataset p
            LEFT JOIN orders o USING (order_id)
            WHERE order_purchase_timestamp IS NOT NULL
            GROUP BY yr, mn
            )
        SELECT
        yr,
        mn,
        monthly_revenue,
        SUM(monthly_revenue) OVER (ORDER BY yr, mn) AS running_total
        FROM monthly_summary
        ORDER BY yr, mn;

        """
        
        rank_customers_lifetime_spend_per_state="""
        select customer_id,customer_state,total,
        Rank() Over(
        partition by customer_state
        order by total DESC) as customer_rank
        from(
        select  customer_id,customer_state, round(sum(payment_value),0) as total
        from (
        select customer_id,customer_state,payment_value
        from clean_orders c 
        right join olist_order_payments_dataset p
        using(order_id)
        left join customers s
        using(customer_id)
        where customer_state is not null) as dd
        group by customer_id,customer_state) as jj;
        """

        month_3rolling_avg="""
        select months,years,total ,round(avg(total) over(partition by years
        order by months
        rows between 2 preceding and current row),0) as rolling_average_3month 
        from(
        select month(order_purchase_timestamp) as months,year(order_purchase_timestamp) as years,round(sum(payment_value),0) as total
        from (
        select * 
        from olist_order_payments_dataset p
        left join clean_orders o 
        using(order_id)
        ) as joined_data
        where order_purchase_timestamp is not null 
        group by months,years
        order by years ,months asc) as dd ;
        """

        # 1- running total revenue by month
        revenue_by_month=run_query(cursor,monthly_revenue)
        print(revenue_by_month)

        # 2- Rank customers by lifetime spend per state 
        rank_customers_by_state= run_query(cursor,rank_customers_lifetime_spend_per_state)
        print(rank_customers_by_state)

        # 3- 3-month rolling average
        month3_roll_avg=run_query(cursor,month_3rolling_avg)
        print(month3_roll_avg)


    except mysql.connector.Error as err:
        print(f'database error: {err}')


    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


        




    
    
    

    
    
    

     
    
    

    
        

    
    
























