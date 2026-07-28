import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# -----------------------------
# MySQL Connection
# -----------------------------
engine = create_engine(
    URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="Ankit@123",
        host="127.0.0.1",
        port=3306,
        database="blinkit_analysis",
    )
)

# -----------------------------
# CSV Folder
# -----------------------------
folder = r"C:\Users\acer\OneDrive\Desktop\blinkit_analysis\data\cleaned"

files = [
    "calendar.csv",
    "coupons.csv",
    "customers.csv",
    "delivery_partners.csv",
    "stores.csv",
    "products.csv",
    "payments.csv",
    "orders.csv",
    "order_items.csv"
]

for file in files:

    table = file.replace(".csv", "")
    path = os.path.join(folder, file)

    print(f"\nLoading {table}...")

    df = pd.read_csv(path)

    # -----------------------------
    # Coupons Fix
    # -----------------------------
    if table == "coupons":
        df.rename(columns={
            "minimum_order": "minimum_order_value",
            "maximum_discount": "discount_value"
        }, inplace=True)

        if "expiry_date" not in df.columns:
            df["expiry_date"] = "2027-12-31"

        if "is_active" not in df.columns:
            df["is_active"] = 1

    # -----------------------------
    # Match MySQL Schema Automatically
    # -----------------------------
    with engine.connect() as conn:
        result = conn.execute(text(f"SHOW COLUMNS FROM {table}"))
        mysql_cols = [row[0] for row in result]

    # Keep only columns that exist in MySQL
    df = df[[c for c in df.columns if c in mysql_cols]]

    # Add missing MySQL columns as NULL
    for col in mysql_cols:
        if col not in df.columns:
            df[col] = None

    # Arrange columns in MySQL order
    df = df[mysql_cols]

    df.to_sql(
        table,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"✅ {table} imported ({len(df):,} rows)")

print("\n🎉 ALL TABLES IMPORTED SUCCESSFULLY!")