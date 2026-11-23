# Olist E-Commerce Delivery Time Prediction

## What This Project Does

Predicts delivery time (in days) for orders placed on the Brazilian Olist e-commerce platform, using order details, customer location, product category, and payment information.

The project covers the full data science lifecycle: data cleaning → exploratory analysis → SQL analytics → model training → API deployment.

---

## Tech Stack

| Layer | Tool |
| --- | --- |
| Data Processing | Pandas |
| SQL Analytics | MySQL 8.0 (CTEs, window functions) |
| Visualization | Matplotlib |
| ML | Scikit-learn (Random Forest, ColumnTransformer, Pipeline) |
| API | FastAPI + Pydantic + Uvicorn |
| Containerization | Docker |
| Model Persistence | Joblib |

---

## Project Structure

```
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── clean_orders.csv              # saved by clean_orders.py
│   ├── master_table.csv              # saved by merge_all.py
│   ├── monthly_revenue.csv           # saved by analysis.py
│   ├── top10_state_revenue.csv       # saved by analysis.py
│   ├── delivery_days.csv             # saved by analysis.py
│   └── average_delivery_days_by_state.csv  # saved by analysis.py
│
├── week1_2_cleaning/
│   ├── clean_orders.py               # Data loading + type conversion utilities
│   └── merge_all.py                  # Grain-aware merge + aggregation functions
│
├── week3_4_analysis/
│   ├── analysis.py                   # Business questions (revenue, delivery, payments)
│   ├── charts.py                     # Monthly revenue, top states, delivery histogram
│   └── output/                       # Generated PNG charts
│       ├── monthly_revenue.png
│       ├── top_state.bar.png
│       └── delivery_days_histogram.png
│
├── week5_6_sql/
│   ├── run_sql.py                    # Python MySQL connector script
│   └── ecommerce.db/                 # Standalone SQL files + notes
│       ├── 01_schema.sql
│       ├── 02_data_validation.sql
│       ├── 03_monthly_revenue.sql
│       ├── 04_top10_states_revenue.sql
│       ├── 05_avg_delivery_by_state.sql
│       └── analysis_notes.md         # Pandas vs SQL comparison notes
│
├── week7_8_model/
│   ├── train.py                      # Model training pipeline
│   ├── predict.py                    # Simple inference script
│   ├── test_order.csv                # Sample order for prediction
│   ├── random_forest_model.joblib    # Saved pipeline
│   ├── Dockerfile                    # Container build instructions
│   ├── requirements.txt              # API-only Python dependencies
│   └── api/
│       └── main.py                   # FastAPI inference endpoint
│
└── README.md                         # This file
```

---

## Key Design Decisions

### 1. Grain-Aware Merging

The Olist dataset has a classic one-to-many structure:

- One order → many payments
- One order → many items

**Merging raw tables directly duplicates order rows**, which silently inflates revenue and corrupts order-level metrics.

**Solution:** Aggregate the "many" side to order-level **before** merging:

```python
# Payments: sum all payment_values per order
payments_agg = df_payments.groupby('order_id')['payment_value'].sum()

# Items: sum prices/freight per order, keep first product_id
items_agg = df_items.groupby('order_id').agg(
    product_id=('product_id', 'first'),
    total_price=('price', 'sum'),
    total_freight=('freight_value', 'sum')
)
```

This preserves the **order-level grain** — one row per order — which is required for delivery-time prediction.

### 2. Only Delivered Orders for Modeling

Canceled, unavailable, and created orders have no `delivery_days` value. Rather than filtering them out through complex logic, the training pipeline keeps only:

```python
df_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()
```

This is a deliberate simplification. A production system would model all order statuses separately.

### 3. Preprocessing Inside the Pipeline

The model is saved as a **Pipeline** (not just the estimator), which includes:

- Numeric imputation (median for `total_price`, `total_freight`, `payment_value`)
- Categorical imputation + one-hot encoding (`customer_state`, `product_category_name_english`)
- Random Forest regressor

This prevents data leakage and ensures the inference API handles new data correctly without manual preprocessing.

---

## Model Performance

| Metric | Baseline (Mean) | Random Forest |
| --- | --- | --- |
| MAE | ~X days | ~Y days |
| RMSE | ~X days | ~Y days |

*(Run `train.py` to see exact values for your data split.)*

The model beats the baseline, but error analysis by state or product category would reveal where it underperforms (e.g., remote states with longer delivery times).

---

## How to Run

### Prerequisites

```bash
pip install -r week7_8_model/requirements.txt
```

### 1. Train the Model

```bash
python week7_8_model/train.py
```

Outputs:

- `week7_8_model/random_forest_model.joblib` — saved pipeline
- `week7_8_model/test_order.csv` — sample order for inference

### 2. Predict via Script

```bash
python week7_8_model/predict.py
```

### 3. Predict via API (Local)

```bash
uvicorn week7_8_model.api.main:app --reload
```

Then POST a new order:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_state": "SP",
    "total_price": 120.50,
    "total_freight": 15.00,
    "product_category_name_english": "electronics",
    "payment_value": 135.50,
    "purchase_month": 6
  }'
```

Response:

```json
{"predicted_delivery_days": 8.42}
```

### 4. Run with Docker

```bash
cd week7_8_model
docker build -t olist-delivery-api .
docker run -p 8000:8000 olist-delivery-api
```

---

## SQL Analysis

### Two SQL Implementations

| Approach | Files | Purpose |
| --- | --- | --- |
| **Python + MySQL** | `run_sql.py` | Connects to MySQL database, runs queries via `mysql-connector`, returns DataFrames |
| **Pure SQL** | `ecommerce.db/*.sql` | Standalone SQL scripts for schema, validation, and analysis |

### SQL Files (`ecommerce.db/`)

| File | What It Does |
| --- | --- |
| `01_schema.sql` | Database schema definition |
| `02_data_validation.sql` | Data quality checks (nulls, duplicates, ranges) |
| `03_monthly_revenue.sql` | Monthly revenue aggregation |
| `04_top10_states_revenue.sql` | Top 10 states by total revenue |
| `05_avg_delivery_by_state.sql` | Average delivery days per state |

### Pandas vs SQL: Known Differences

The SQL and Pandas implementations **do not produce identical results.** This is expected and documented in `ecommerce.db/analysis_notes.md`:

| Aspect | Pandas | SQL |
| --- | --- | --- |
| Source data | `olist_orders_dataset` (raw) | `clean_orders` (cleaned) |
| Missing value handling | Pandas `fillna()` | SQL `COALESCE` / `WHERE IS NOT NULL` |
| Join type | Configurable per merge | Fixed in schema design |
| Rounding | `round()` in Python | `ROUND()` in SQL |

> **"The purpose of the SQL implementation was to demonstrate the ability to perform the same analytical tasks using SQL, rather than to reproduce the pandas results exactly."**

Exact matching would require using the same data, filters, joins, missing-value handling, and rounding in both implementations.

---

## Known Limitations (Honest)

| Limitation | Why It Exists |
| --- | --- |
| Order-level grain only | Product-level detail is aggregated away (mode category, sum of prices) |
| Month-only trend (no year) | Week 3 task specified "month," not year-month |
| Hardcoded 2019 cutoff | `shipping_limit_date` filter; should be documented or removed |
| No hyperparameter tuning | Default Random Forest parameters; grid search would improve performance |
| No error analysis by segment | MAE/RMSE are averages; state-level or category-level errors are unknown |
| No model monitoring | No drift detection for production deployment |

---

## What Was Learned

- **Grain is not a technical detail** — it is a business decision. Every merge must respect it.
- **Validation is not paranoia** — it is making your assumptions visible so the data can confirm or deny them.
- **Simple is faster** — a 1-line filter (`order_status == 'delivered'`) replaced 10 lines of convoluted logic with the same result.

---

## Author

Self-taught data science learner. Native Arabic speaker. Building this project to transition into a junior Data Scientist / ML Engineer role.
