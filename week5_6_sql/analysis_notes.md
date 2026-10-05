# SQL Analysis Notes

The SQL analysis reproduces three analyses previously performed in pandas:

1. Monthly revenue
2. Top 10 states by total revenue
3. Average delivery days by state

The results show small differences because the two implementations did not use exactly the same source data.

* **Pandas:** used the original `olist_orders_dataset`
* **SQL:** used the cleaned `clean_orders` table

Since `clean_orders` was cleaned and contains slightly different data, small differences in the results are expected.

The purpose of the SQL implementation was to demonstrate the ability to perform the same analytical tasks using SQL, rather than to reproduce the pandas results exactly.

**Note:** Exact matching would require using the same data, filters, joins, missing-value handling, and rounding in both implementations.
