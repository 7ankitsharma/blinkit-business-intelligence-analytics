# 🛒 Blinkit Business Intelligence Analysis

An end-to-end data analytics project simulating a quick-commerce (Blinkit-style) business — from raw data generation through cleaning, validation, SQL-based business analysis, and an interactive 5-page Power BI dashboard.

![Executive Dashboard](assets/Executive.png)

---

## 📌 Project Overview

This project analyzes the full lifecycle of a quick-commerce operation — customers, products, orders, deliveries, and payments — to answer real business questions around **revenue growth, delivery SLA performance, customer retention, and product profitability**.

**Pipeline:**

```
Synthetic Data Generation (Python) 
        ↓
Data Cleaning & Validation (Jupyter Notebook)
        ↓
MySQL Database (Schema + Load)
        ↓
Business Queries (SQL)
        ↓
Power BI Dashboard (5 interactive pages)
```

**Scale:** ~1,000,000 orders · 250,000 customers · 8,000 products · 120 stores · 15,000 delivery partners

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Data Generation | Python, Pandas, NumPy, Faker |
| Data Cleaning & Validation | Jupyter Notebook, Pandas |
| Database | MySQL 8.0, SQLAlchemy, PyMySQL |
| Business Analysis | SQL (CTEs, Window Functions) |
| Visualization | Power BI |

---

## 📁 Project Structure

```
blinkit-analysis/
│
├── data/
│   ├── raw/                          # Raw generated CSVs (not included — see below)
│   └── cleaned/                      # Cleaned CSVs used for MySQL load
│
├── python/
│   ├── dataset.py                    # Generates synthetic Blinkit dataset (9 CSVs)
│   ├── 01_Data_Validation.ipynb      # Cleans & validates raw data
│   └── 03_load_data.py               # Loads cleaned CSVs into MySQL
│
├── sql/
│   ├── 01_create_database.sql        # Creates the blinkit_analysis database
│   ├── 02_create_tables.sql          # Defines table schemas (orders, customers, etc.)
│   ├── 03_business_queries.sql       # Core business queries (generic MySQL)
│   └── 05_business_queries_mysql.sql # Refined/corrected version of business queries
│
├── dashboard/
│   └── Blinkit_Business_Intelligence_Dashboard.pbix
│
├── Dashboard_Screenshots/
│   ├── Executive.png
│   ├── Customers.png
│   ├── Delivery_and_operations.png
│   ├── Delivery_partners.png
│   └── Product.png
│
└── README.md
```

> **Note:** Raw CSVs are excluded from the repo due to size (~1M+ rows). Run `dataset.py` to regenerate them locally.

---

## ⚙️ How to Run

**1. Generate the dataset**
```bash
pip install pandas numpy faker
python scripts/dataset.py
```
This creates 9 CSV files: `calendar`, `products`, `customers`, `stores`, `delivery_partners`, `coupons`, `orders`, `order_items`, `payments`.

**2. Clean & validate the data**

Open and run `scripts/01_Data_Validation.ipynb` to check for nulls, duplicates, referential integrity, and outliers, and produce the cleaned CSVs used downstream.

**3. Set up the MySQL database**
```bash
mysql -u root -p < sql/01_create_database.sql
mysql -u root -p < sql/02_create_tables.sql
```

**4. Load cleaned data into MySQL**
```bash
pip install sqlalchemy pymysql
python scripts/03_load_data.py
```
> Update the DB credentials and the `folder` path in `03_load_data.py` before running.

**5. Run the business queries**

Execute `sql/05_business_queries_mysql.sql` in MySQL Workbench (or your client of choice) to reproduce all KPIs feeding the dashboard.

**6. Explore the dashboard**

Open `dashboard/Blinkit_Business_Intelligence_Dashboard.pbix` in Power BI Desktop.

---

## 🗃️ Data Model

| Table | Description |
|---|---|
| `customers` | Demographics, membership tier, acquisition channel |
| `products` | Catalog with pricing, brand, category, GST |
| `stores` | Dark store locations and warehouse capacity |
| `delivery_partners` | Partner details and ratings |
| `coupons` | Discount codes and rules |
| `calendar` | Date dimension with holidays/festivals |
| `orders` | Order-level facts: value, status, delivery times, SLA |
| `order_items` | Line-item detail per order |
| `payments` | Payment method, status, gateway |

---

## 📊 Business Questions Answered

**Revenue**
- Month-over-month revenue growth & AOV trends
- Revenue share by city and membership tier
- Revenue and profit margin by product category

**Operations**
- SLA breach rate by weather & traffic conditions
- Hourly demand patterns and delivery speed
- Store utilization / warehouse stress index

**Customers**
- RFM segmentation (Recency, Frequency, Monetary)
- Cohort retention by signup month
- Customer lifetime value by acquisition channel

**Products**
- Top-selling products per category
- Market basket analysis (frequently bought together)
- Pareto (80/20) revenue concentration

**Logistics & Finance**
- Delivery partner performance & SLA compliance
- Coupon effectiveness on basket size
- Weekend vs. weekday sales
- Cancellation reasons and lost GMV

---

## 📈 Dashboard Preview

**Executive Overview** — Revenue, profit, cancellation rate, and category performance at a glance
![Executive](assets/Executive.png)

**Customer Insights & Retention** — Segmentation, signup trends, acquisition channels
![Customers](assets/Customers.png)

**Delivery & Operations** — SLA compliance, delivery time trends, hourly order volume
![Delivery and Operations](assets/Delivery_and_operations.png)

**Delivery Partner Performance** — Ratings, vehicle mix, city-wise partner distribution
![Delivery Partners](assets/Delivery_partners.png)

**Product & Inventory Intelligence** — Top products, brand performance, margin analysis
![Product](assets/Product.png)

---

## 🔑 Key Insights

- ~63% of orders meet SLA overall, but breach rates spike above 90% in **rainy weather regardless of traffic level**, pointing to weather as the dominant delivery-time risk factor.
- **70% of customers hold a Normal membership**, but Plus/Premium tiers likely carry disproportionate revenue share — a natural upsell target.
- Dairy & Breakfast and Snacks & Munchies are the top two revenue categories, together contributing close to $2bn of total revenue.
- Peak order volume occurs consistently between **6 PM–9 PM**, suggesting staffing and inventory should be weighted toward evening demand.

*(Replace/expand with your own numbers as your analysis evolves.)*

---

## 🚀 Future Improvements

- Automate the pipeline with Airflow or a scheduled script
- Add a Streamlit app for ad-hoc query exploration
- Incorporate real-time or near-real-time data refresh into Power BI

---

## 👤 Author

Ankit , https://github.com/7ankitsharma
