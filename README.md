# Olist E-Commerce Analysis

### Project Overview
## DATASET:

The Olist Brazilian E-Commerce dataset contains approximately 100,000 orders made between 2016 and 2018 through the Olist marketplace in Brazil.
It includes information about orders, customers, products, payments, sellers, and deliveries, 
allowing analysis of sales performance, customer behavior, and delivery operations.

## Clone the repository
```bash
git clone https://github.com/Mohammed-DSML/ecommerce-project.git 
cd ecommerce-project
```
## Installation

Run the following command in Bash:
```bash
pip install -r requirements.txt
```
## Run the scripts

Run the scripts from the project root in the following order:
```bash
python -m week1_2_cleaning.clean_orders
python -m week1_2_cleaning.merge_all
python -m week3_4_analysis.analysis
python -m week3_4_analysis.charts.charts
```
The scripts generate the cleaned data, analytical outputs, and charts used in the project.

## Analysis Summary

The analysis revealed several notable patterns in revenue, delivery, and payment behavior.

Monthly revenue varied throughout the year, with May recording the highest revenue and September the lowest.

Revenue was highly concentrated in three states, with São Paulo generating substantially more revenue than Rio de Janeiro and Minas Gerais. 

Average delivery times also varied considerably across states, ranging from 8 days in São Paulo to almost 29 days in Roraima. 

Approximately 8% of delivered orders arrived after the estimated delivery date. 

Credit cards were the dominant payment method, accounting for around 73% of payments, followed by boleto at approximately 19%.

